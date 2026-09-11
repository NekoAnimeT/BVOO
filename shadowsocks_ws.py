# shadowsocks_ws.py — Shadowsocks TLS/WebSocket inbound for OXNET
import asyncio
import hashlib
import secrets
from datetime import datetime

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from fastapi import WebSocket, WebSocketDisconnect

from main import (
    LINKS, LINKS_LOCK, stats, connections, error_logs, logger,
    is_link_allowed, save_state, resolve_link_id,
)
from relay_vless import check_and_use

KEY_LEN = 32
SALT_LEN = 32
TAG_LEN = 16
NONCE_LEN = 12
INFO = b"ss-subkey"


def _evp_bytes_to_key(password: str, key_len: int = KEY_LEN) -> bytes:
    data = password.encode()
    out = b""
    prev = b""
    while len(out) < key_len:
        prev = hashlib.md5(prev + data).digest()
        out += prev
    return out[:key_len]


def _derive_subkey(password: str, salt: bytes) -> bytes:
    return HKDF(algorithm=hashes.SHA1(), length=KEY_LEN, salt=salt, info=INFO).derive(_evp_bytes_to_key(password))


def _nonce(counter: int) -> bytes:
    return counter.to_bytes(NONCE_LEN, "little")


class SSDecryptor:
    def __init__(self, password: str):
        self.buf = bytearray()
        self.aead = None
        self.counter = 0
        self.password = password

    def feed(self, data: bytes) -> list[bytes]:
        self.buf.extend(data)
        out = []
        if self.aead is None:
            if len(self.buf) < SALT_LEN:
                return out
            salt = bytes(self.buf[:SALT_LEN]); del self.buf[:SALT_LEN]
            self.aead = ChaCha20Poly1305(_derive_subkey(self.password, salt))
        while True:
            if len(self.buf) < 2 + TAG_LEN:
                break
            enc_len = bytes(self.buf[:2 + TAG_LEN])
            plen = int.from_bytes(self.aead.decrypt(_nonce(self.counter), enc_len, b""), "big")
            if plen > 0x3FFF:
                raise ValueError("invalid ss chunk length")
            if len(self.buf) < 2 + TAG_LEN + plen + TAG_LEN:
                break
            del self.buf[:2 + TAG_LEN]
            self.counter += 1
            enc_payload = bytes(self.buf[:plen + TAG_LEN]); del self.buf[:plen + TAG_LEN]
            payload = self.aead.decrypt(_nonce(self.counter), enc_payload, b"")
            self.counter += 1
            if payload:
                out.append(payload)
        return out


class SSEncryptor:
    def __init__(self, password: str):
        self.salt = secrets.token_bytes(SALT_LEN)
        self.aead = ChaCha20Poly1305(_derive_subkey(password, self.salt))
        self.counter = 0
        self.started = False

    def encrypt_chunk(self, payload: bytes) -> bytes:
        parts = []
        if not self.started:
            parts.append(self.salt)
            self.started = True
        for i in range(0, len(payload), 0x3FFF):
            chunk = payload[i:i + 0x3FFF]
            parts.append(self.aead.encrypt(_nonce(self.counter), len(chunk).to_bytes(2, "big"), b""))
            self.counter += 1
            parts.append(self.aead.encrypt(_nonce(self.counter), chunk, b""))
            self.counter += 1
        return b"".join(parts)


def _ws_client_ip(ws: WebSocket) -> str:
    fwd = ws.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = ws.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return ws.client.host if ws.client else "نامشخص"


def parse_ss_header(chunk: bytes):
    if len(chunk) < 7:
        raise ValueError("chunk too small for ss header")
    pos = 0
    atyp = chunk[pos]; pos += 1
    if atyp == 1:
        address = ".".join(str(b) for b in chunk[pos:pos+4]); pos += 4
    elif atyp == 3:
        ln = chunk[pos]; pos += 1
        address = chunk[pos:pos+ln].decode("utf-8", errors="ignore"); pos += ln
    elif atyp == 4:
        ab = chunk[pos:pos+16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown ss atyp: {atyp}")
    port = int.from_bytes(chunk[pos:pos+2], "big"); pos += 2
    return address, port, chunk[pos:]


async def _ss_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, conn_id: str, uid: str, decryptor: SSDecryptor):
    while True:
        msg = await ws.receive()
        if msg["type"] == "websocket.disconnect":
            break
        data = msg.get("bytes") or (msg.get("text") or "").encode()
        for plain in decryptor.feed(data):
            if not await check_and_use(uid, len(plain)):
                await ws.close(code=1008, reason="quota/disabled")
                return
            connections[conn_id]["bytes"] += len(plain)
            writer.write(plain)
            if writer.transport.get_write_buffer_size() > 512 * 1024:
                await writer.drain()


async def _tcp_to_ss_ws(ws: WebSocket, reader: asyncio.StreamReader, conn_id: str, uid: str, encryptor: SSEncryptor):
    while True:
        data = await reader.read(256 * 1024)
        if not data:
            break
        if not await check_and_use(uid, len(data)):
            await ws.close(code=1008, reason="quota/disabled")
            return
        connections[conn_id]["bytes"] += len(data)
        await ws.send_bytes(encryptor.encrypt_chunk(data))


async def shadowsocks_ws_tunnel(ws: WebSocket, uuid: str):
    await ws.accept()
    uid = await resolve_link_id(uuid)
    async with LINKS_LOCK:
        link = LINKS.get(uid) if uid else None
    if not is_link_allowed(link):
        await ws.close(code=1008, reason="not authorized")
        return

    ip = _ws_client_ip(ws)
    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {"uuid": uid, "ip": ip, "transport": "shadowsocks-tls", "connected_at": datetime.now().isoformat(), "bytes": 0}
    writer = None
    try:
        decryptor = SSDecryptor(uid)
        first_plain = None
        while first_plain is None:
            msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
            if msg["type"] == "websocket.disconnect":
                return
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            chunks = decryptor.feed(data)
            if chunks:
                first_plain = b"".join(chunks)
        if not await check_and_use(uid, len(first_plain)):
            await ws.close(code=1008, reason="quota/disabled")
            return
        address, port, payload = parse_ss_header(first_plain)
        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_plain)
        reader, writer = await asyncio.wait_for(asyncio.open_connection(address, port), timeout=10.0)
        sock = writer.transport.get_extra_info('socket')
        if sock:
            import socket
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if payload:
            writer.write(payload)
            await writer.drain()
        encryptor = SSEncryptor(uid)
        done, pending = await asyncio.wait({
            asyncio.create_task(_ss_ws_to_tcp(ws, writer, conn_id, uid, decryptor)),
            asyncio.create_task(_tcp_to_ss_ws(ws, reader, conn_id, uid, encryptor)),
        }, return_when=asyncio.FIRST_COMPLETED)
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass
        asyncio.create_task(save_state())
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": f"ss-tls: {exc}", "time": datetime.now().isoformat()})
        logger.error(f"SS-TLS error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close(); await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
