# trojan.py
# ══════════════════════════════════════════════════════════════════════════════
# Trojan Relay — همون معماری relay_vless.py، منتها auth بر پایه‌ی پروتکل Trojan
#  پسورد Trojan = همون UUID کانفیگ (SHA224 آن، طبق اسپک پروتکل Trojan)
#  چون پسورد داخل استریم اول فرستاده می‌شه (نه در URL)، روی هش، بین UUIDهای
#  فعال جستجو می‌کنیم و لینک متناظر رو پیدا می‌کنیم.
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import hashlib
import secrets
import socket
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from main import (
    LINKS,
    LINKS_LOCK,
    stats,
    connections,
    error_logs,
    logger,
    is_link_allowed,
    save_state,
    log_activity,
)
from relay_vless import check_and_use, relay_ws_to_tcp, relay_tcp_to_ws

RELAY_BUF = 256 * 1024
TROJAN_HEADER_MIN = 56 + 2 + 1 + 1 + 1 + 2 + 2  # hash+CRLF+cmd+atyp+min_addr+port+CRLF


def _ws_client_ip(ws: WebSocket) -> str:
    fwd = ws.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = ws.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return ws.client.host if ws.client else "نامشخص"


def trojan_hash(password: str) -> str:
    """طبق اسپک Trojan: hex(SHA224(password)) — این‌جا password = UUID کانفیگ."""
    return hashlib.sha224(password.encode()).hexdigest()


async def find_uuid_by_trojan_hash(pw_hash: str) -> str | None:
    async with LINKS_LOCK:
        for uid in LINKS:
            if trojan_hash(uid) == pw_hash:
                return uid
    return None


async def parse_trojan_header(chunk: bytes):
    """
    فرمت Trojan:
      56 bytes hex(SHA224(password)) + CRLF + CMD(1) + ATYP(1) + ADDR + PORT(2) + CRLF + payload
    """
    if len(chunk) < TROJAN_HEADER_MIN:
        raise ValueError("chunk too small for trojan header")

    pw_hash = chunk[:56].decode("ascii", errors="ignore")
    pos = 56

    if chunk[pos:pos + 2] != b"\r\n":
        raise ValueError("invalid trojan header: missing CRLF after hash")
    pos += 2

    command = chunk[pos]; pos += 1
    atyp = chunk[pos]; pos += 1

    if atyp == 1:  # IPv4
        address = ".".join(str(b) for b in chunk[pos:pos + 4]); pos += 4
    elif atyp == 3:  # domain
        dlen = chunk[pos]; pos += 1
        address = chunk[pos:pos + dlen].decode("utf-8", errors="ignore"); pos += dlen
    elif atyp == 4:  # IPv6
        ab = chunk[pos:pos + 16]; pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown trojan atyp: {atyp}")

    port = int.from_bytes(chunk[pos:pos + 2], "big"); pos += 2

    if chunk[pos:pos + 2] != b"\r\n":
        raise ValueError("invalid trojan header: missing trailing CRLF")
    pos += 2

    return pw_hash, command, address, port, chunk[pos:]


async def _resolve_and_authorize(first_chunk: bytes):
    """هش پسورد رو پارس و به UUID مچ می‌کنه؛ اگر مجاز نبود None برمی‌گردونه."""
    pw_hash, command, address, port, payload = await parse_trojan_header(first_chunk)
    uuid = await find_uuid_by_trojan_hash(pw_hash)
    async with LINKS_LOCK:
        link = LINKS.get(uuid) if uuid else None
    if not is_link_allowed(link):
        return None, None, None, None, None
    return uuid, address, port, payload, len(first_chunk)


async def trojan_ws_tunnel(ws: WebSocket):
    """
    اندپوینت وب‌سوکت Trojan. عمداً {uuid} در URL نداره — طبق اسپک واقعی Trojan
    پسورد داخل استریم اول (بعد از هندشیک TLS) فرستاده می‌شه، نه در مسیر.
    """
    await ws.accept()
    ip = _ws_client_ip(ws)
    conn_id = secrets.token_urlsafe(6)
    writer = None
    uuid = None

    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        uuid, address, port, payload, hlen = await _resolve_and_authorize(first_chunk)
        if uuid is None:
            logger.warning(f" Trojan-WS rejected [{conn_id}] ip={ip} (not authorized)")
            await ws.close(code=1008, reason="not authorized")
            return

        async with LINKS_LOCK:
            link = LINKS.get(uuid)

        connections[conn_id] = {
            "uuid": uuid,
            "ip": ip,
            "transport": "trojan-ws",
            "connected_at": datetime.now().isoformat(),
            "bytes": 0,
        }
        logger.info(f" Trojan-WS [{conn_id}] uuid={uuid[:8]}… ip={ip} total={len(connections)}")
        log_activity("connection", f"اتصال Trojan جدید از {ip} (کانفیگ {link.get('label','?')})", "info")

        if not await check_and_use(uuid, hlen):
            await ws.close(code=1008, reason="quota/disabled")
            return

        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += hlen
        logger.info(f"️  [{conn_id}] Trojan → {address}:{port}")

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port), timeout=10.0
        )
        sock = writer.transport.get_extra_info("socket")
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        if payload:
            writer.write(payload)
            await writer.drain()

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uuid)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, conn_id, uuid, vless_prefix=False)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state())

    except WebSocketDisconnect as exc:
        logger.info(f"Trojan-WS [{conn_id}] client disconnected early: code={getattr(exc,'code',None)} reason={getattr(exc,'reason',None)}")
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "trojan connection timeout", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error(f"Trojan-WS error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
        logger.info(f" Trojan-WS closed [{conn_id}] total={len(connections)}")
