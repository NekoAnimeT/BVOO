import asyncio
import json
import os
import hashlib
import secrets
import sys
import re
import time
import aiofiles
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from collections import deque, defaultdict
from pathlib import Path
import mtproto
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("app")

IRAN_TZ = ZoneInfo("Asia/Tehran")

app = FastAPI(title="App", docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Persistence ───────────────────────────────────────────────────────────────
def _resolve_data_dir() -> Path:
    """
    Prefer Railway Volume mount. Order:
      1) DATA_DIR env
      2) /data  (mount a Railway Volume here)
      3) ./data next to the app
      4) /tmp/oxnet-data (last resort — lost on redeploy)
    """
    candidates: list[Path] = []
    env = (os.environ.get("DATA_DIR") or "").strip()
    if env:
        candidates.append(Path(env))
    candidates.append(Path("/data"))
    candidates.append(Path(__file__).resolve().parent / "data")
    candidates.append(Path("/tmp/oxnet-data"))
    for p in candidates:
        try:
            p.mkdir(parents=True, exist_ok=True)
            probe = p / ".oxnet_write_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            return p
        except Exception:
            continue
    return Path("/tmp/oxnet-data")


DATA_DIR = _resolve_data_dir()
DATA_FILE = DATA_DIR / "oxnet_state.json"
SECRET_FILE = DATA_DIR / ".oxnet_secret"
PANEL_VERSION_FILE = Path(__file__).with_name("version.txt")
SAVE_LOCK = asyncio.Lock()
logger.info(f"DATA_DIR={DATA_DIR} (mount a Volume on /data to survive redeploys)")


def _get_or_create_secret() -> str:
    """اولویت با Environment Variable — برای Free tier (Koyeb و …) ضروری است.
    مقدار secret هرگز در لاگ چاپ نمی‌شود.
    """
    env_secret = (os.environ.get("SECRET_KEY") or "").strip()
    if env_secret:
        logger.info("SECRET_KEY از Environment Variable بارگذاری شد.")
        return env_secret
    # بدون env: رفتار قبلی development (فایل یا موقت) + هشدار
    logger.warning(
        "SECRET_KEY در Environment تنظیم نشده؛ روی Free Hostingهای ephemeral "
        "(مثل Koyeb بدون Volume) بعد از ری‌استارت ممکن است Login خراب شود. "
        "SECRET_KEY ثابت در env تنظیم کنید."
    )
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SECRET_FILE.exists():
            val = SECRET_FILE.read_text(encoding="utf-8").strip()
            if val:
                return val
        new_secret = secrets.token_urlsafe(32)
        SECRET_FILE.write_text(new_secret, encoding="utf-8")
        logger.info("SECRET_KEY جدید ساخته و در دیسک ذخیره شد (پایدار بین ری‌استارت‌ها).")
        return new_secret
    except Exception as e:
        logger.warning(f"عدم امکان ذخیره‌ی SECRET_KEY روی دیسک: {e} — از مقدار موقت استفاده می‌شود.")
        return secrets.token_urlsafe(32)


CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": _get_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}


def get_current_panel_version() -> str:
    try:
        if PANEL_VERSION_FILE.exists():
            for line in PANEL_VERSION_FILE.read_text(encoding="utf-8").splitlines():
                if line.startswith("version="):
                    return line.split("=", 1)[1].strip() or "1.0.0"
    except Exception:
        pass
    return "1.0.0"


def _state_snapshot() -> dict:
    return {
        "links": dict(LINKS),
        "subs": dict(SUBS),
        "customers": dict(CUSTOMERS),
        "settings": dict(SETTINGS),
        "nodes": dict(NODES),
        "password_hash": AUTH["password_hash"],
        "hourly_traffic": dict(hourly_traffic),
        "stats": {
            "total_bytes": stats.get("total_bytes", 0),
            "total_requests": stats.get("total_requests", 0),
            "total_errors": stats.get("total_errors", 0),
        },
        "saved_at": datetime.now().isoformat(),
    }


def _as_bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        return v.strip().lower() in ("1", "true", "yes", "on", "active", "فعال")
    return bool(v)


def _normalize_active_flags():
    for link in LINKS.values():
        if isinstance(link, dict) and "active" in link:
            link["active"] = _as_bool(link.get("active", True))
    for sub in SUBS.values():
        if isinstance(sub, dict) and "active" in sub:
            sub["active"] = _as_bool(sub.get("active", True))


async def load_state():
    global LINKS, AUTH, SUBS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = None
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw) if raw.strip() else None
        if data:
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            CUSTOMERS.update(data.get("customers", {}))
            SETTINGS.update(data.get("settings", {}))
            SETTINGS.setdefault("cloudflare", {"domains": []})
            SETTINGS.setdefault("panel", {"domain": "", "login_path": ""})
            SETTINGS.setdefault("extra_domains", [])
            SETTINGS.setdefault("railway_tcp", {"domain": "", "port": 0, "path_mode": "panel"})
            SETTINGS.setdefault("reality", {"host": "", "port": 443, "pbk": "", "sid": "", "sni": "", "fp": "chrome", "spx": "/"})
            SETTINGS.setdefault("telegram", {
                "bot_token": "", "admin_id": "", "backup_every_min": 10,
                "notify_quota": True, "notify_node_down": True, "enabled": False,
                "last_backup_at": "", "last_ok": False,
            })
            SETTINGS.setdefault("node_health", {
                "interval_sec": 120, "fail_threshold": 2, "sub_skip_offline": True,
            })
            SETTINGS.setdefault("cluster", {
                "role": "standalone", "node_name": "", "region": "",
                "central_url": "",
                "central_url_secondary": "", "node_token": "", "cluster_secret": "", "auto_sync": True,
            })
            if isinstance(data.get("nodes"), dict):
                NODES.clear()
                NODES.update(data.get("nodes") or {})
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            ht = data.get("hourly_traffic") or {}
            if isinstance(ht, dict):
                for k, v in ht.items():
                    try:
                        hourly_traffic[str(k)] += int(v or 0)
                    except Exception:
                        pass
            st = data.get("stats") or {}
            if isinstance(st, dict):
                stats["total_bytes"] = int(st.get("total_bytes") or stats.get("total_bytes") or 0)
                stats["total_requests"] = int(st.get("total_requests") or stats.get("total_requests") or 0)
                stats["total_errors"] = int(st.get("total_errors") or stats.get("total_errors") or 0)
            _normalize_active_flags()
            logger.info(f"State loaded from JSON: {len(LINKS)} links, {len(SUBS)} subs")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")
    try:
        rebuild_path_index()
    except Exception:
        pass

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = _state_snapshot()
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ── In-memory state ───────────────────────────────────────────────────────────
connections: dict = {}
stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
http_client: httpx.AsyncClient | None = None
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()
CUSTOMERS: dict = {}
CUSTOMERS_LOCK = asyncio.Lock()
SETTINGS: dict = {
    "theme": {"accent": "#2563EB", "radius": 16, "density": "comfortable", "mode": "light"},
    "security": {"lockout_enabled": True, "max_attempts": 5, "lock_minutes": 10, "allowed_ips": []},
    "cleanup": {"auto_delete_expired_days": 0, "inactive_archive_days": 0, "log_keep": 150, "low_resource": False},
    "panel": {"domain": "", "login_path": ""},
    "cloudflare": {"domains": []},
    "extra_domains": [],
    # Railway TCP Proxy → public domain:port for VLESS WS without TLS
    "railway_tcp": {
        "domain": "",          # e.g. yamabiko.proxy.rlwy.net
        "port": 0,             # e.g. 49391
        "path_mode": "root",   # root = / (Railway sample) | panel = /ws/{path}
    },
    # VLESS Reality share-link params (client URI generation)
    "reality": {
        "host": "",            # IP or hostname (e.g. 66.33.22.241)
        "port": 443,
        "pbk": "",             # public key (auto-generated)
        "sid": "",             # short id (auto-generated)
        "sni": "",             # server name (auto-generated from pool)
        "fp": "chrome",
        "spx": "/",
        "private_key": "",     # x25519 private (kept server-side)
    },
    "smart_profiles": {
        "general": ["trojan-ws", "vless-ws", "xhttp-stream-up"],
        "mobile": ["trojan-ws", "vless-ws", "shadowsocks-tls"],
        "mci": ["trojan-ws", "vless-ws"],
        "irancell": ["vless-ws", "trojan-ws", "xhttp-stream-up"],
        "wifi": ["xhttp-stream-up", "trojan-ws", "vless-ws"],
    },
    # نام کانفیگ‌ها در ساب (remark بعد از #)
    # متغیرها: {label} {username} {status} {status_emoji} {remain_traffic} {total_traffic}
    #          {used_traffic} {remain_time} {remain_days} {protocol} {target} {domain}
    #          {cdn} {flag} {sub_name}
    "remark_template": "{status_emoji} {label} · {target}",
    # خطوط آماری بالای هر ساب (کانفیگ‌های نمایشی)
    "info_templates": [
        "{status_emoji} وضعیت اشتراک: {status}",
        "👤 کاربر: {username}",
        "📦 حجم باقیمانده: {remain_traffic} از {total_traffic}",
        "⏰ زمان باقیمانده: {remain_time}",
    ],
    "info_configs_enabled": True,
    # پنل مرکزی / نود (چند منطقه Railway)
    "cluster": {
        "role": "standalone",   # standalone | central | node
        "node_name": "",
        "region": "",           # us-east | us-west | nl | sg | custom
        "central_url": "",      # https://central.example.com
        "central_url_secondary": "",  # fallback if primary down
        "node_token": "",       # توکن اختصاصی این نود
        "cluster_secret": "",   # فقط روی مرکزی — برای ثبت نود جدید
        "auto_sync": True,
        # هنگام ارسال به مرکزی کدام دامنه ساخته شود
        "sync_main": True,      # دامنه اصلی پنل نود
        "sync_extra": True,     # دامنه‌های فرعی + IP/دامنه تمیز
        "sync_cf": False,       # دامنه‌های کلادفلیر نود (اختیاری)
    },
    "telegram": {
        "bot_token": "",
        "admin_id": "",
        "backup_every_min": 10,
        "notify_quota": True,
        "notify_node_down": True,
        "enabled": False,
        "last_backup_at": "",
        "last_ok": False,
    },
    "node_health": {
        "interval_sec": 120,
        "fail_threshold": 2,
        "sub_skip_offline": True,
    },
}
# نودهای ثبت‌شده روی پنل مرکزی: id -> meta + configs
NODES: dict = {}
# sub_id -> set of connection keys (ip+ua hash) for device limit
DEVICE_CONN_INDEX: dict = {}

NODES_LOCK = asyncio.Lock()
FAILED_LOGINS: dict = {}

PROTOCOLS = (
    "vless-ws",
    "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one",
    "trojan-ws",
    "trojan-xhttp-packet-up", "trojan-xhttp-stream-up",
    "shadowsocks-tls", "mtproto", "multi",
    "vless-tcp",      # VLESS WS via Railway TCP Proxy (no TLS)
    "vless-reality",  # VLESS Reality (TCP) share link
)
DEFAULT_PROTOCOL = "vless-ws"

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })


# ── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "sid"
SESSION_TTL = 60 * 60 * 24 * 7

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "123456"))}

def security_client_allowed(ip: str) -> bool:
    allowed = SETTINGS.get("security", {}).get("allowed_ips") or []
    return not allowed or ip in allowed

def is_login_locked(ip: str) -> tuple[bool, int]:
    sec = SETTINGS.get("security", {})
    if not sec.get("lockout_enabled", True):
        return False, 0
    rec = FAILED_LOGINS.get(ip) or {"count": 0, "until": 0}
    until = float(rec.get("until") or 0)
    if until > time.time():
        return True, int(until - time.time())
    return False, 0

def record_login_failure(ip: str):
    sec = SETTINGS.get("security", {})
    max_attempts = int(sec.get("max_attempts", 5) or 5)
    lock_minutes = int(sec.get("lock_minutes", 10) or 10)
    rec = FAILED_LOGINS.setdefault(ip, {"count": 0, "until": 0})
    rec["count"] = int(rec.get("count", 0)) + 1
    if rec["count"] >= max_attempts:
        rec["until"] = time.time() + lock_minutes * 60
        rec["count"] = 0

def record_login_success(ip: str):
    FAILED_LOGINS.pop(ip, None)

SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token

async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True

async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token

# ── Startup / Shutdown ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(
        limits=limits, timeout=timeout, follow_redirects=True,
    )
    asyncio.create_task(_cluster_auto_sync_loop())
    asyncio.create_task(_telegram_backup_loop())
    asyncio.create_task(_node_health_loop())
    asyncio.create_task(_quota_notify_loop())
    asyncio.create_task(_central_watchdog_loop())
    await load_state()
    await _restart_mtproto_instances()
    log_activity("system", "سرور راه‌اندازی شد", "ok")
    logger.info(f"app listening on {CONFIG['port']}")

async def _restart_mtproto_instances():
    async with LINKS_LOCK:
        targets = [
            (uid, d) for uid, d in LINKS.items()
            if d.get("protocol") == "mtproto" and d.get("active", True)
        ]
    for uid, d in targets:
        try:
            inst = await mtproto.start_instance(
                uid,
                secret=d.get("mtproto_secret"),
                domain=d.get("mtproto_domain", mtproto.DEFAULT_FAKE_TLS_DOMAIN),
                preferred_port=d.get("mtproto_port"),
                force_port=d.get("mtproto_manual_port", False),
                ad_tag=d.get("ad_tag"),
            )
            old_port = d.get("mtproto_port")
            async with LINKS_LOCK:
                LINKS[uid]["mtproto_port"] = inst["port"]
                LINKS[uid]["mtproto_secret"] = inst["secret"]

            if (d.get("mtproto_proxy_id") and inst["port"] != old_port
                    and not d.get("mtproto_manual_port", False)):
                asyncio.create_task(_reattach_mtproto_public_proxy(
                    uid, inst["port"], d.get("mtproto_proxy_id"), d.get("label", "")
                ))
        except Exception as exc:
            logger.error(f"ری‌استارت خودکار MTProto ناموفق برای {uid[:8]}: {exc}")

async def _mtproto_usage_callback(uuid: str, n_bytes: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if link is None:
            return False
        if not is_link_allowed(link):
            return False
        link["used_bytes"] += n_bytes
        stats["total_bytes"] += n_bytes
        bump_hourly(n_bytes)
        _charge_local_link_to_sub(uuid, n_bytes)
    # اگر این پنل نود است، مصرف را به مرکزی بفرست
    if _cluster_role() == "node":
        asyncio.create_task(report_usage_to_central_multi(uuid, n_bytes))
    return True

mtproto.set_usage_callback(_mtproto_usage_callback)

async def _attach_mtproto_public_proxy(uid: str, application_port: int, label: str):
    async with LINKS_LOCK:
        if uid in LINKS:
            LINKS[uid]["mtproto_public_pending"] = False
    await save_state()

async def _reattach_mtproto_public_proxy(uid: str, new_port: int, old_proxy_id: Optional[str], label: str):
    await _attach_mtproto_public_proxy(uid, new_port, label)

# ===== تابع جدید برای به‌روزرسانی ad_tag روی پروکسی =====
async def _update_mtproto_ad_tag(uuid: str, ad_tag: str):
    try:
        await mtproto.stop_instance(uuid)
        async with LINKS_LOCK:
            link = LINKS.get(uuid)
            if not link:
                return
            inst = await mtproto.start_instance(
                uuid,
                secret=link.get("mtproto_secret"),
                domain=link.get("mtproto_domain", mtproto.DEFAULT_FAKE_TLS_DOMAIN),
                preferred_port=link.get("mtproto_port"),
                force_port=link.get("mtproto_manual_port", False),
                ad_tag=ad_tag,
            )
            link["mtproto_port"] = inst["port"]
            link["mtproto_secret"] = inst["secret"]
            link["ad_tag"] = ad_tag
            link["ad_tag_status"] = "done"          # ← جدید
            link["ad_tag_link"] = generate_share_link(   # ← جدید، لینک تازه با سکرت جدید
                uuid, get_host(), remark=f"{link.get('label','')}", protocol="mtproto"
            )
        await save_state()            # ذخیره فوری در دیتابیس/دیسک
        logger.info(f"MTProto[{uuid[:8]}]: ad_tag به‌روز شد و instance ری‌استارت شد")
    except Exception as exc:
        logger.error(f"خطا در به‌روزرسانی ad_tag برای {uuid[:8]}: {exc}")
        async with LINKS_LOCK:
            if uuid in LINKS:
                LINKS[uuid]["active"] = False
                LINKS[uuid]["ad_tag_status"] = "error"
        log_activity("link", f"به‌روزرسانی ad_tag برای «{LINKS.get(uuid,{}).get('label','')}» ناموفق بود", "err")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    await mtproto.stop_all()
    if http_client:
        await http_client.aclose()

# ── Helpers ───────────────────────────────────────────────────────────────────
def normalize_config_path(value: str | None) -> str | None:
    """Return a clean user-facing path token such as PlanAsli for /ws/PlanAsli."""
    if value is None:
        return None
    value = str(value).strip().strip('/')
    if value.startswith('ws/'):
        value = value[3:]
    if not value:
        return None
    value = re.sub(r'\s+', '-', value)
    value = re.sub(r'[^A-Za-z0-9._-]', '', value)[:64]
    if len(value) < 2:
        return None
    return value


PATH_INDEX: dict[str, str] = {}

def rebuild_path_index() -> None:
    global PATH_INDEX
    idx_map: dict[str, str] = {}
    for uid, link in LINKS.items():
        p = str(link.get("path") or "").strip().strip("/")
        if p:
            idx_map[p] = uid
        idx_map[uid] = uid
        alias = str(link.get("cluster_uuid_alias") or "").strip()
        if alias:
            idx_map[alias] = uid
        for a in (link.get("uuid_aliases") or []):
            if a:
                idx_map[str(a)] = uid
    PATH_INDEX = idx_map

async def resolve_link_id(token: str) -> str | None:
    """Resolve either the original UUID or the custom path to the internal UUID."""
    if not token:
        return None
    hit = PATH_INDEX.get(token)
    if hit and hit in LINKS:
        return hit
    async with LINKS_LOCK:
        if token in LINKS:
            return token
        for uid, link in LINKS.items():
            if link.get('path') == token:
                return uid
            if str(link.get('cluster_uuid_alias') or '') == token:
                return uid
            if token in [str(x) for x in (link.get('uuid_aliases') or [])]:
                return uid
    return None

async def unique_config_path(base: str | None, fallback: str) -> str:
    base = normalize_config_path(base) or fallback
    async with LINKS_LOCK:
        used = {uid for uid in LINKS} | {str(v.get('path')) for v in LINKS.values() if v.get('path')}
    candidate = base
    i = 2
    while candidate in used:
        candidate = f"{base}-{i}"
        i += 1
    return candidate

def proto_slug(proto: str) -> str:
    return proto.replace('shadowsocks-tls', 'ss').replace('trojan-', 'tr-').replace('vless-', 'vl-').replace('xhttp-', 'xh-').replace('-up', '').replace('-one', '1')


def normalize_login_path(value: str | None) -> str:
    """Slug for custom login URL: /{slug}/login. Empty = default /login."""
    if value is None:
        return ""
    value = str(value).strip().strip("/")
    value = re.sub(r"^https?://", "", value, flags=re.I).split("/", 1)[0] if "://" in str(value) else value
    value = value.strip().strip("/")
    # only path segment characters
    value = re.sub(r"[^A-Za-z0-9._-]", "", value)[:64]
    # reserve system paths
    reserved = {
        "api", "login", "dashboard", "health", "stats", "sub", "sub-all", "sub-group",
        "p", "ws", "proxy", "cf-sub", "domain-sub", "xhttp-siz10", "trojan-ws", "ss",
        "docs", "redoc", "openapi.json", "test-ws",
    }
    if not value or value.lower() in reserved or len(value) < 4:
        return ""
    return value


def get_login_path() -> str:
    panel = SETTINGS.get("panel") or {}
    return normalize_login_path(panel.get("login_path") or "")


def get_panel_base() -> str:
    """Prefix for panel routes when secret path is set, e.g. /mysecret"""
    slug = get_login_path()
    return f"/{slug}" if slug else ""


def get_login_url() -> str:
    base = get_panel_base()
    return f"{base}/login" if base else "/login"


def get_dashboard_url() -> str:
    base = get_panel_base()
    return f"{base}/dashboard" if base else "/dashboard"


def get_host() -> str:
    raw = str((SETTINGS.get("panel") or {}).get("domain") or "").strip()
    if raw:
        raw = re.sub(r"^https?://", "", raw, flags=re.I).split("/", 1)[0].strip().strip(".")
        if raw:
            return raw
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


_REALITY_SNI_POOL = [
    "www.cloudflare.com",
    "www.microsoft.com",
    "www.samsung.com",
    "www.apple.com",
    "gateway.icloud.com",
    "dl.google.com",
    "www.amazon.com",
    "cdn.jsdelivr.net",
]


def generate_reality_params() -> dict:
    """Generate Reality client params: x25519 keypair + random sid/sni/spx."""
    import base64
    private_key = ""
    public_key = ""
    try:
        from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
        from cryptography.hazmat.primitives import serialization
        priv = X25519PrivateKey.generate()
        priv_raw = priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_raw = priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        private_key = base64.urlsafe_b64encode(priv_raw).decode().rstrip("=")
        public_key = base64.urlsafe_b64encode(pub_raw).decode().rstrip("=")
    except Exception:
        # Fallback: random 32-byte values (client-format only; no real Reality server)
        private_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
        public_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")

    sid = secrets.token_hex(secrets.choice([2, 4, 6, 8]))
    sni = secrets.choice(_REALITY_SNI_POOL)
    spx = "/" + secrets.token_hex(8)
    return {
        "pbk": public_key,
        "private_key": private_key,
        "sid": sid,
        "sni": sni,
        "fp": "chrome",
        "spx": spx,
    }


def ensure_reality_params() -> dict:
    """Fill missing Reality fields with generated values (keeps host/port)."""
    real = SETTINGS.setdefault("reality", {})
    need = not real.get("pbk") or not real.get("sid") or not real.get("sni")
    if need:
        gen = generate_reality_params()
        for k, v in gen.items():
            if not real.get(k):
                real[k] = v
        if not real.get("fp"):
            real["fp"] = "chrome"
        if not real.get("spx"):
            real["spx"] = gen.get("spx") or "/"
    return real

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)


def hourly_bucket_key(dt: datetime | None = None) -> str:
    dt = dt or now_ir()
    return dt.strftime("%Y-%m-%d %H:00")


def bump_hourly(n: int):
    try:
        hourly_traffic[hourly_bucket_key()] += int(n or 0)
    except Exception:
        pass


def hourly_last_n(hours: int = 24) -> dict:
    now = now_ir().replace(minute=0, second=0, microsecond=0)
    out: dict[str, int] = {}
    for i in range(hours - 1, -1, -1):
        t = now - timedelta(hours=i)
        key_new = t.strftime("%Y-%m-%d %H:00")
        key_old = t.strftime("%H:00")
        val = int(hourly_traffic.get(key_new, 0) or 0)
        if val == 0 and t.date() == now.date():
            val = int(hourly_traffic.get(key_old, 0) or 0)
        label = t.strftime("%H:00")
        # if duplicate hour labels, prefix with day
        if label in out:
            label = t.strftime("%m/%d %H:00")
        out[label] = val
    return out


def _uri_authority_host(host: str) -> str:
    host = str(host or "").strip()
    if host.startswith("[") and host.endswith("]"):
        return host
    # IPv6 literals must be bracketed in URI authority: vless://uuid@[IPv6]:443
    if ":" in host and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", host):
        return f"[{host}]"
    return host

def generate_share_link(uuid: str, host: str, remark: str = "OXNET", protocol: str = DEFAULT_PROTOCOL, sni_host: str | None = None, port: int = 443, credential_uuid: str | None = None) -> str:
    link_obj = LINKS.get(uuid, {})
    public_path = link_obj.get("path") or uuid
    public_uuid = credential_uuid or link_obj.get("cluster_uuid_alias") or uuid
    tls_host = (sni_host or host).strip()
    authority_host = _uri_authority_host(host)
    # port 80 = plain HTTP / no TLS for clients that support it; 443 = TLS
    use_tls = int(port) != 80
    security = "tls" if use_tls else "none"

    # ── VLESS via Railway TCP Proxy (WS, no TLS) ─────────────────────────────
    # Example:
    # vless://uuid@yamabiko.proxy.rlwy.net:49391?path=%2Fws%2Fxxx&security=none&encryption=none&type=ws#name
    if protocol == "vless-tcp":
        tcp = SETTINGS.get("railway_tcp") or {}
        t_host = (link_obj.get("tcp_domain") or tcp.get("domain") or host or "").strip()
        t_host = re.sub(r"^https?://", "", t_host, flags=re.I).split("/", 1)[0].strip()
        try:
            t_port = int(link_obj.get("tcp_port") or tcp.get("port") or 0)
        except (TypeError, ValueError):
            t_port = 0
        if not t_port:
            t_port = int(port) if port else 443
        path_mode = str(link_obj.get("tcp_path_mode") or tcp.get("path_mode") or "root").strip().lower()
        # Default root=/ matches working Railway samples (UUID is in VLESS header)
        if path_mode == "panel":
            wspath = f"/{str(public_path).lstrip('/')}"
        else:
            wspath = "/"
        params = {
            "encryption": "none",
            "security": "none",
            "type": "ws",
            "path": wspath,
        }
        query = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params.items())
        tag = remark or "node"
        return f"vless://{public_uuid}@{_uri_authority_host(t_host)}:{t_port}?{query}#{quote(tag)}"

    # ── VLESS Reality (TCP) share link ───────────────────────────────────────
    # Example:
    # vless://uuid@IP:PORT?security=reality&encryption=none&pbk=...&fp=chrome&spx=%2F...&type=tcp&sni=...&sid=...#name
    if protocol == "vless-reality":
        r = SETTINGS.get("reality") or {}
        r_host = (link_obj.get("reality_host") or r.get("host") or host or "").strip()
        r_host = re.sub(r"^https?://", "", r_host, flags=re.I).split("/", 1)[0].strip()
        try:
            r_port = int(link_obj.get("reality_port") or r.get("port") or 443)
        except (TypeError, ValueError):
            r_port = 443
        pbk = str(link_obj.get("reality_pbk") or r.get("pbk") or "").strip()
        sid = str(link_obj.get("reality_sid") or r.get("sid") or "").strip()
        sni = str(link_obj.get("reality_sni") or r.get("sni") or "").strip()
        fp = str(link_obj.get("reality_fp") or r.get("fp") or "chrome").strip() or "chrome"
        spx = str(link_obj.get("reality_spx") or r.get("spx") or "/").strip() or "/"
        params = {
            "security": "reality",
            "encryption": "none",
            "pbk": pbk,
            "headerType": "",
            "fp": fp,
            "spx": spx,
            "type": "tcp",
            "sni": sni,
            "sid": sid,
        }
        query = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params.items())
        tag = remark or "node"
        return f"vless://{public_uuid}@{_uri_authority_host(r_host)}:{r_port}?{query}#{quote(tag)}"

    # path همیشه فقط /{token} تصادفی — بدون /ws /xhttp-siz10 /trojan-ws
    clean_path = f"/{str(public_path).lstrip('/')}"

    if protocol == "shadowsocks-tls":
        import base64
        user = base64.urlsafe_b64encode(f"chacha20-ietf-poly1305:{public_uuid}".encode()).decode().rstrip("=")
        if use_tls:
            plugin = quote(f"v2ray-plugin;tls;mode=websocket;host={tls_host};path={clean_path}", safe="")
        else:
            plugin = quote(f"v2ray-plugin;mode=websocket;host={tls_host};path={clean_path}", safe="")
        tag = remark or "node"
        if not use_tls:
            tag = f"{tag}-HTTP80"
        return f"ss://{user}@{authority_host}:{int(port)}?plugin={plugin}#{quote(tag)}"
    if protocol == "mtproto":
        link = LINKS.get(uuid)
        mport = link.get("mtproto_port") if link else None
        secret = link.get("mtproto_secret") if link else None
        if not mport or not secret:
            return f"tg://proxy?server={host}&port=0&secret=not_ready#{quote(remark)}"
        pub_host = link.get("mtproto_public_host") if link else None
        pub_port = link.get("mtproto_public_port") if link else None
        final_host = pub_host or host
        final_port = pub_port or mport
        return mtproto.generate_mtproto_link(final_host, final_port, secret)
    if protocol == "trojan-ws":
        params = {
            "security": security, "type": "ws", "host": tls_host,
            "path": clean_path, "fp": "chrome", "alpn": "http/1.1",
        }
        if use_tls:
            params["sni"] = tls_host
        query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        tag = remark if use_tls else f"{remark}-HTTP80"
        return f"trojan://{public_uuid}@{authority_host}:{int(port)}?{query}#{quote(tag)}"
    if protocol.startswith("trojan-xhttp-"):
        mode = protocol.replace("trojan-xhttp-", "")
        if mode == "stream-one":
            mode = "stream-up"
        r_path = f"/r/{str(public_path).lstrip('/')}"
        params = {
            "security": security, "type": "xhttp", "mode": mode, "host": tls_host,
            "path": r_path, "fp": "chrome", "alpn": "h2,http/1.1",
        }
        if use_tls:
            params["sni"] = tls_host
        query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        tag = remark if use_tls else f"{remark}-HTTP80"
        return f"trojan://{public_uuid}@{authority_host}:{int(port)}?{query}#{quote(tag)}"
    if protocol == "vless-ws":
        # WebSocket: path ساده /token
        params = {
            "encryption": "none",
            "security": security,
            "type": "ws",
            "host": tls_host,
            "path": clean_path,
            "fp": "chrome",
            "alpn": "http/1.1",
        }
        if use_tls:
            params["sni"] = tls_host
    elif protocol.startswith("xhttp-") or "xhttp" in protocol:
        mode = protocol.replace("xhttp-", "").replace("trojan-", "")
        if mode == "stream-one":
            mode = "stream-up"
        if mode not in ("packet-up", "stream-up", "stream-one"):
            mode = "stream-up"
        r_path = f"/r/{str(public_path).lstrip('/')}"
        params = {
            "encryption": "none",
            "security": security,
            "type": "xhttp",
            "mode": mode,
            "host": tls_host,
            "path": r_path,
            "fp": "chrome",
            "alpn": "h2,http/1.1",
        }
        if use_tls:
            params["sni"] = tls_host
    else:
        # سایر پروتکل‌های ناشناخته: fallback به WS path ساده
        params = {
            "encryption": "none",
            "security": security,
            "type": "ws",
            "host": tls_host,
            "path": clean_path,
            "fp": "chrome",
            "alpn": "http/1.1",
        }
        if use_tls:
            params["sni"] = tls_host
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    tag = remark if use_tls else f"{remark}-HTTP80"
    return f"vless://{public_uuid}@{authority_host}:{int(port)}?{query}#{quote(tag)}"

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB": return int(value * 1024 ** 3)
    if unit == "MB": return int(value * 1024 ** 2)
    if unit == "KB": return int(value * 1024)
    return int(value)

def _as_bool(val) -> bool:
    """Normalize JSON/bool/string flags to real bool."""
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    if isinstance(val, (int, float)):
        return val != 0
    s = str(val).strip().lower()
    if s in ("1", "true", "yes", "on", "active"):
        return True
    if s in ("0", "false", "no", "off", "inactive", ""):
        return False
    return bool(val)


def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def _sub_effective_limit(sub: dict | None) -> int:
    """سقف حجم اشتراک: limit_bytes خود ساب، وگرنه بزرگ‌ترین limit کانفیگ‌های محلی‌اش."""
    if not sub:
        return 0
    try:
        sl = int(sub.get("limit_bytes") or 0)
    except Exception:
        sl = 0
    if sl > 0:
        return sl
    best = 0
    for lid in sub.get("link_ids") or []:
        lid = str(lid)
        if _is_remote_link_id(lid):
            continue
        link = LINKS.get(lid)
        if not link:
            continue
        try:
            lb = int(link.get("limit_bytes") or 0)
        except Exception:
            lb = 0
        if lb > best:
            best = lb
    return best


def _sub_used_bytes(sub: dict | None) -> int:
    if not sub:
        return 0
    try:
        return int(sub.get("used_bytes") or 0)
    except Exception:
        return 0


def _sub_quota_exceeded(sub: dict | None) -> bool:
    lim = _sub_effective_limit(sub)
    if lim <= 0:
        return False
    return _sub_used_bytes(sub) >= lim


def is_link_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not _as_bool(link.get("active", True)):
        return False
    if is_link_expired(link):
        return False
    # اگر مرکزی سهمیه نود را پر اعلام کرده
    if link.get("central_quota_exceeded"):
        return False
    lb = link.get("limit_bytes", 0)
    try:
        lb = int(lb or 0)
    except Exception:
        lb = 0
    used = link.get("used_bytes", 0)
    try:
        used = int(used or 0)
    except Exception:
        used = 0
    if lb > 0 and used >= lb:
        return False
    # ساب والد / گروه مولتی + سهمیه تجمیعی اشتراک
    sub_id = link.get("sub_id")
    multi_id = link.get("multi_group_id")
    if sub_id:
        sub = SUBS.get(sub_id)
        if sub is None:
            return False
        if _as_bool(sub.get("active", True)) is False:
            return False
        if _sub_quota_exceeded(sub):
            return False
    if multi_id:
        msub = SUBS.get(multi_id)
        if msub is None:
            return False
        if _as_bool(msub.get("active", True)) is False:
            return False
        if _sub_quota_exceeded(msub):
            return False
    return True

def _fmt_remain_time(link: dict) -> tuple[str, str]:
    """Returns (remain_time_text, remain_days_text)."""
    exp = link.get("expires_at")
    if not exp:
        return "∞", "∞"
    try:
        end = datetime.fromisoformat(exp)
        if end.tzinfo is None:
            now = datetime.now()
        else:
            now = datetime.now(end.tzinfo)
        delta = end - now
        if delta.total_seconds() <= 0:
            return "منقضی", "0"
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"{days} روز و {hours} ساعت", str(days)
        mins = (delta.seconds % 3600) // 60
        return f"{hours} ساعت و {mins} دقیقه", "0"
    except Exception:
        return "—", "—"


def build_remark_context(
    link: dict,
    *,
    target: str = "",
    domain: str = "",
    sub: dict | None = None,
    cdn: bool = False,
    cdn_name: str = "",
    extra_name: str = "",
) -> dict:
    label = str(link.get("label") or "کانفیگ")
    username = str(
        link.get("username")
        or link.get("user")
        or ((sub or {}).get("name") if sub else "")
        or label
    )
    active = is_link_allowed(link)
    status = "فعال" if active else "غیرفعال"
    status_emoji = "🟢" if active else "🔴"
    used = int(link.get("used_bytes") or 0)
    limit = int(link.get("limit_bytes") or 0)
    remain = max(limit - used, 0) if limit > 0 else -1
    remain_traffic = "∞" if limit <= 0 else fmt_bytes(remain)
    total_traffic = "∞" if limit <= 0 else fmt_bytes(limit)
    used_traffic = fmt_bytes(used)
    remain_time, remain_days = _fmt_remain_time(link)
    proto = str(link.get("protocol") or DEFAULT_PROTOCOL)
    tgt = target or domain or get_host()
    extra = str(extra_name or cdn_name or "").strip()
    cdn_label = extra or (str(domain) if cdn else "")
    return {
        "label": label,
        "username": username,
        "status": status,
        "status_emoji": status_emoji,
        "remain_traffic": remain_traffic,
        "total_traffic": total_traffic,
        "used_traffic": used_traffic,
        "remain_time": remain_time,
        "remain_days": remain_days,
        "protocol": proto,
        "target": tgt,
        "domain": domain or tgt,
        "cdn": "CDN" if (cdn or extra) else "",
        "cdn_name": extra or cdn_label,
        "extra_name": extra or cdn_label,
        "flag": str(link.get("flag") or ""),
        "sub_name": str((sub or {}).get("name") or ""),
    }


def apply_template(template: str, ctx: dict) -> str:
    text = template or ""
    for k, v in ctx.items():
        text = text.replace("{" + k + "}", str(v))
    # clean double spaces / separators
    text = re.sub(r"\s*·\s*·\s*", " · ", text)
    text = re.sub(r"\s{2,}", " ", text).strip(" ·-")
    return text.strip() or ctx.get("label") or "OXNET"


def format_config_remark(
    link: dict,
    *,
    target: str = "",
    domain: str = "",
    sub: dict | None = None,
    cdn: bool = False,
    cdn_name: str = "",
    extra_name: str = "",
) -> str:
    tmpl = (SETTINGS.get("remark_template") or "{status_emoji} {label} · {target}").strip()
    ctx = build_remark_context(
        link, target=target, domain=domain, sub=sub, cdn=cdn,
        cdn_name=cdn_name, extra_name=extra_name,
    )
    return apply_template(tmpl, ctx)

def build_info_config_lines(link: dict, sub: dict | None = None, host: str | None = None) -> list[str]:
    """Display-only share lines (dummy endpoint) for subscription stats."""
    if not SETTINGS.get("info_configs_enabled", True):
        return []
    templates = SETTINGS.get("info_templates")
    if not isinstance(templates, list) or not templates:
        return []
    host = host or get_host()
    ctx = build_remark_context(link, target=host, domain=host, sub=sub, cdn=False)
    # one context for whole sub: prefer first link's quota or aggregate? use this link
    fake = "00000000-0000-0000-0000-000000000001"
    lines = []
    for tmpl in templates:
        t = str(tmpl or "").strip()
        if not t:
            continue
        remark = apply_template(t, ctx)
        lines.append(
            f"vless://{fake}@{host}:1?encryption=none&security=none&type=ws&path=%2Finfo#{quote(remark)}"
        )
    return lines


def build_sub_info_lines(links: list[dict], sub: dict | None, host: str) -> list[str]:
    """Stats lines once per subscription (use first allowed link or sub aggregate)."""
    if not SETTINGS.get("info_configs_enabled", True):
        return []
    if not links:
        # still show sub-level if possible
        dummy = {
            "label": (sub or {}).get("name") or "اشتراک",
            "active": bool(sub and sub.get("active", True)),
            "limit_bytes": 0,
            "used_bytes": 0,
            "protocol": "info",
        }
        return build_info_config_lines(dummy, sub=sub, host=host)
    # aggregate used/limit across links
    base = dict(links[0])
    total_used = sum(int(l.get("used_bytes") or 0) for l in links)
    limits = [int(l.get("limit_bytes") or 0) for l in links]
    if any(x > 0 for x in limits):
        total_limit = sum(x for x in limits if x > 0)
    else:
        total_limit = 0
    base["used_bytes"] = total_used
    base["limit_bytes"] = total_limit
    base["label"] = (sub or {}).get("name") or base.get("label") or "اشتراک"
    # earliest expiry
    exp_dates = []
    for l in links:
        if l.get("expires_at"):
            try:
                exp_dates.append(datetime.fromisoformat(l["expires_at"]))
            except Exception:
                pass
    if exp_dates:
        base["expires_at"] = min(exp_dates).isoformat()
    return build_info_config_lines(base, sub=sub, host=host)

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "نامشخص"

# ── Default link ──────────────────────────────────────────────────────────────
_default_link_created = False

async def ensure_default_link():
    global _default_link_created
    if _default_link_created:
        return
    async with LINKS_LOCK:
        if not any(l.get("is_default") for l in LINKS.values()):
            uid = hashlib.sha256(f"default{CONFIG['secret']}".encode()).hexdigest()
            uid = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
            if uid not in LINKS:
                LINKS[uid] = {
                    "label": "لینک پیش‌فرض",
                    "limit_bytes": 0,
                    "used_bytes": 0,
                    "created_at": datetime.now().isoformat(),
                    "active": True,
                    "expires_at": None,
                    "note": "",
                    "is_default": True,
                    "sub_id": None,
                    "protocol": DEFAULT_PROTOCOL,
                    "path": uid,
                }
                await save_state()
        _default_link_created = True

# ── Basic endpoints ───────────────────────────────────────────────────────────
@app.get("/")
async def root():
    # پاسخ عمومی شبیه اپ عادی — بدون نام محصول/پروتکل
    return {"ok": True}

@app.get("/health")
@app.get("/healthz")
@app.get("/ready")
async def health():
    return {"status": "ok"}

# ── Subscription (single link) ────────────────────────────────────────────────
@app.get("/sub/{uuid}")
async def subscription_single(uuid: str):
    import base64
    uid = await resolve_link_id(uuid)
    if not uid:
        raise HTTPException(status_code=404, detail="not found or inactive")
    async with LINKS_LOCK:
        link = LINKS.get(uid)
    if not link or not is_link_allowed(link):
        raise HTTPException(status_code=404, detail="not found or inactive")
    host = get_host()
    sub = SUBS.get(link.get("sub_id")) if link.get("sub_id") else None
    lines = build_sub_info_lines([link], sub, host) + _share_lines_for_all_domains(uid, link, host, sub=sub)
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain",
                    headers={"profile-title": quote(link["label"])})

@app.get("/sub-all")
async def subscription_all(_=Depends(require_auth)):
    import base64
    host = get_host()
    async with LINKS_LOCK:
        lines = []
        for uid, d in LINKS.items():
            if is_link_allowed(d):
                lines.extend(_share_lines_for_all_domains(uid, d, host))
    # On a central panel, node-provided share URIs are first-class members of /sub-all.
    if _cluster_role() == "central":
        async with NODES_LOCK:
            for node in NODES.values():
                for cfg in node.get("configs") or []:
                    if isinstance(cfg, dict) and _as_bool(cfg.get("active", True)):
                        uri = str(cfg.get("uri") or "").strip()
                        if uri:
                            lines.append(uri)
    # Keep the subscription deterministic and remove accidental duplicate URIs.
    lines = list(dict.fromkeys(lines))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")

# ══════════════════════════════════════════════════════════════════════════════
# SUB GROUP endpoints (بدون تغییر)
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = (body.get("name") or "گروه جدید").strip()[:60]
    desc = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    # سقف حجم اشتراک (برای کسر مصرف نودها از همین گیگ)
    limit_bytes = 0
    try:
        if body.get("limit_bytes") is not None:
            limit_bytes = int(body.get("limit_bytes") or 0)
        elif body.get("limit_value") is not None:
            limit_bytes = 0 if float(body.get("limit_value") or 0) <= 0 else parse_size_to_bytes(
                float(body.get("limit_value") or 0), body.get("limit_unit") or "GB"
            )
    except Exception:
        limit_bytes = 0
    sub_id = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "name": name,
            "desc": desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key": uuid_key,
            "created_at": datetime.now().isoformat(),
            "link_ids": [],
            "active": True,
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
        }
    await save_state()
    log_activity("sub", f"گروه «{name}» ساخته شد", "ok")
    host = get_host()
    return {
        "sub_id": sub_id,
        **SUBS[sub_id],
        "public_url": f"https://{host}/p/{uuid_key}",
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
    }

@app.get("/api/subs")
async def list_subs(_=Depends(require_auth)):
    host = get_host()
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        link_ids = s.get("link_ids", [])
        active_count = 0
        local_used = 0
        for lid in link_ids:
            lid = str(lid)
            if _is_remote_link_id(lid):
                cfg = _resolve_remote_config(lid)
                if cfg and _as_bool(cfg.get("active", True)):
                    active_count += 1
                continue
            if is_link_allowed(snap_links.get(lid)):
                active_count += 1
            if lid in snap_links:
                local_used += int(snap_links[lid].get("used_bytes") or 0)
        # مصرف تجمیعی اشتراک (نود+محلی) اولویت دارد
        try:
            sub_used = int(s.get("used_bytes") or 0)
        except Exception:
            sub_used = 0
        total_used = max(sub_used, local_used)
        sub_limit = _sub_effective_limit(s)
        result.append({
            "sub_id": sid,
            **s,
            "password_hash": None,
            "has_password": s.get("password_hash") is not None,
            "active": s.get("active", True),
            "links_count": len(link_ids),
            "active_count": active_count,
            "total_used_bytes": total_used,
            "total_used_fmt": fmt_bytes(total_used),
            "limit_bytes": sub_limit,
            "limit_fmt": "∞" if sub_limit <= 0 else fmt_bytes(sub_limit),
            "quota_exceeded": _sub_quota_exceeded(s),
            "public_url": f"https://{host}/p/{s['uuid_key']}",
            "sub_url": f"https://{host}/sub-group/{s['uuid_key']}",
            "cloudflare_subs": cloudflare_sub_urls_for_key(host, s["uuid_key"]),
            "domain_subs": domain_sub_urls_for_key(host, s["uuid_key"]),
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}

def _is_remote_link_id(lid: str) -> bool:
    return str(lid or "").startswith("remote:")


def _resolve_remote_config(lid: str) -> dict | None:
    """remote:{node_id}:{source_id|idx} → dict با uri واقعی نود (بدون ساخت UUID محلی)."""
    raw = str(lid or "")
    if not raw.startswith("remote:"):
        return None
    parts = raw.split(":", 2)
    if len(parts) < 3:
        return None
    _, node_id, src = parts
    node = NODES.get(node_id)
    if not node:
        return None
    for idx, cfg in enumerate(node.get("configs") or []):
        if not isinstance(cfg, dict):
            continue
        key = str(cfg.get("source_id") if cfg.get("source_id") not in (None, "") else idx)
        if key == src:
            uri = str(cfg.get("uri") or "").strip()
            if not uri:
                return None
            return {
                "uri": uri,
                "label": cfg.get("label") or "Node config",
                "protocol": cfg.get("protocol") or "",
                "active": _as_bool(cfg.get("active", True)),
                "node_id": node_id,
                "node_name": node.get("name") or "Node",
                "node_region": node.get("region") or "",
                "source_id": key,
            }
    return None


def _collect_sub_share_lines(sub: dict, host: str) -> tuple[list[str], list[dict]]:
    """خطوط share برای یک ساب: لینک‌های محلی + URIهای نود (بدون بازنویسی UUID نود)."""
    if _sub_quota_exceeded(sub):
        return [], []
    link_ids = list(sub.get("link_ids") or [])
    allowed_links: list[dict] = []
    lines: list[str] = []
    sub_used = _sub_used_bytes(sub)
    sub_lim = _sub_effective_limit(sub)
    for lid in link_ids:
        lid = str(lid)
        if _is_remote_link_id(lid):
            try:
                if not is_remote_link_eligible(lid):
                    continue
            except Exception:
                pass
            cfg = _resolve_remote_config(lid)
            if not cfg or not _as_bool(cfg.get("active", True)):
                continue
            uri = cfg.get("uri") or ""
            canonical = str(sub.get("unified_uuid") or "").strip()
            if uri and canonical and uri.startswith(("vless://", "trojan://")):
                uri = re.sub(r"^([a-zA-Z0-9+.-]+://)[^@]+@", lambda m: m.group(1) + canonical + "@", uri, count=1)
            if uri:
                lines.append(uri)
                allowed_links.append({
                    "label": cfg.get("label"),
                    "used_bytes": int(cfg.get("used_bytes") or 0) or sub_used,
                    "limit_bytes": sub_lim,
                    "active": True,
                    "remote_node": True,
                })
            continue
        link = LINKS.get(lid)
        if link and is_link_allowed(link):
            allowed_links.append(link)
            lines.extend(_share_lines_for_all_domains(lid, link, host, sub=sub))
    lines = list(dict.fromkeys(lines))
    pref = list(sub.get("preferred_protocols") or [])
    if pref:
        try:
            lines = _sort_lines_by_protocol_pref(lines, pref)
        except Exception:
            pass
    return lines, allowed_links


def _charge_sub_usage(sub_id: str, n: int) -> None:
    """مصرف را روی اشتراک مرکزی + یک کانفیگ محلی دارای سقف می‌نویسد."""
    if n <= 0 or not sub_id:
        return
    sub = SUBS.get(sub_id)
    if not sub:
        return
    sub["used_bytes"] = int(sub.get("used_bytes") or 0) + n
    for lid in sub.get("link_ids") or []:
        lid = str(lid)
        if _is_remote_link_id(lid):
            continue
        link = LINKS.get(lid)
        if not link:
            continue
        try:
            lb = int(link.get("limit_bytes") or 0)
        except Exception:
            lb = 0
        if lb > 0:
            link["used_bytes"] = int(link.get("used_bytes") or 0) + n
            break


def _charge_local_link_to_sub(uuid: str, n: int) -> None:
    """مصرف رله محلی را به used_bytes اشتراک والد هم اضافه کن."""
    if n <= 0:
        return
    link = LINKS.get(uuid)
    if not link:
        return
    for sid in (link.get("sub_id"), link.get("multi_group_id")):
        if sid and sid in SUBS:
            SUBS[sid]["used_bytes"] = int(SUBS[sid].get("used_bytes") or 0) + n


async def report_usage_to_central(uuid: str, n_bytes: int) -> None:
    """نود → مرکزی: گزارش بایت برای کسر از اشتراک مرکزی."""
    if n_bytes <= 0:
        return
    if _cluster_role() != "node":
        return
    c = _cluster()
    central = (c.get("central_url") or "").strip().rstrip("/")
    token = (c.get("node_token") or "").strip()
    if not central or not token:
        return
    if not central.startswith("http"):
        central = "https://" + central
    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            r = await client.post(
                f"{central}/api/cluster/usage",
                headers={"X-Node-Token": token, "Authorization": f"Bearer {token}"},
                json={"uuid": uuid, "source_id": uuid, "bytes": int(n_bytes)},
            )
            if r.status_code >= 400:
                return
            data = r.json() if r.content else {}
            if data.get("allowed") is False:
                async with LINKS_LOCK:
                    if uuid in LINKS:
                        LINKS[uuid]["central_quota_exceeded"] = True
                await save_state()
            elif data.get("allowed") is True:
                async with LINKS_LOCK:
                    if uuid in LINKS and LINKS[uuid].get("central_quota_exceeded"):
                        LINKS[uuid]["central_quota_exceeded"] = False
    except Exception as exc:
        logger.debug("report_usage_to_central failed: %s", exc)


def _set_remote_active(lid: str, active: bool) -> bool:
    """active را روی کانفیگ نود در NODES ست می‌کند. True اگر پیدا شد."""
    raw = str(lid or "")
    if not raw.startswith("remote:"):
        return False
    parts = raw.split(":", 2)
    if len(parts) < 3:
        return False
    _, node_id, src = parts
    node = NODES.get(node_id)
    if not node:
        return False
    found = False
    for idx, cfg in enumerate(node.get("configs") or []):
        if not isinstance(cfg, dict):
            continue
        key = str(cfg.get("source_id") if cfg.get("source_id") not in (None, "") else idx)
        if key == src:
            cfg["active"] = bool(active)
            found = True
    return found


def _sync_sub_link_ids(sub_id: str, new_ids: list) -> int:
    """فقط membership همین ساب را عوض می‌کند — از ساب‌های دیگر (مثل Fam/Me) دزدی نمی‌کند.
    remote و local هر دو می‌توانند در چند ساب همزمان باشند.
    """
    new_set = []
    seen = set()
    for lid in new_ids or []:
        lid = str(lid)
        if not lid or lid in seen:
            continue
        if _is_remote_link_id(lid):
            # remote حتی اگر نود موقتاً آفلاین باشد قابل ذخیره است
            seen.add(lid)
            new_set.append(lid)
            continue
        if lid in LINKS:
            seen.add(lid)
            new_set.append(lid)

    changed = 0
    # مهم: لیست بقیه ساب‌ها دست نخورده می‌ماند (باگ Me↔Fam)
    old_ids = set(SUBS[sub_id].get("link_ids") or [])
    SUBS[sub_id]["link_ids"] = new_set
    new_ids_set = set(new_set)

    for lid, link in LINKS.items():
        if not isinstance(link, dict):
            continue
        if lid in new_ids_set:
            # نمایش primary: اگر sub_id خالی بود یا همین ساب بود، همین را بگذار
            if not link.get("sub_id") or link.get("sub_id") == sub_id:
                if link.get("sub_id") != sub_id:
                    link["sub_id"] = sub_id
                    changed += 1
        elif link.get("sub_id") == sub_id and lid in old_ids and lid not in new_ids_set:
            # از این ساب حذف شد — اگر هنوز در ساب دیگری هست به آن اشاره کن
            other = next(
                (sid for sid, s in SUBS.items()
                 if sid != sub_id and lid in (s.get("link_ids") or [])),
                None,
            )
            link["sub_id"] = other
            changed += 1
    return changed


@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    deactivated = False
    reactivated = False
    membership_changed = 0
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        if "name" in body:
            s["name"] = str(body["name"])[:60]
        if "desc" in body:
            s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "limit_bytes" in body:
            try:
                s["limit_bytes"] = max(0, int(body.get("limit_bytes") or 0))
            except Exception:
                pass
        if "limit_value" in body:
            try:
                lv = float(body.get("limit_value") or 0)
                s["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, body.get("limit_unit") or "GB")
            except Exception:
                pass
        if body.get("reset_usage"):
            s["used_bytes"] = 0
        if "link_ids" in body:
            async with LINKS_LOCK:
                membership_changed = _sync_sub_link_ids(sub_id, list(body.get("link_ids") or []))
            # اگر ساب سقف نداشت، از کانفیگ‌های محلی‌اش بگیر
            if int(s.get("limit_bytes") or 0) <= 0:
                derived = _sub_effective_limit(s)
                if derived > 0:
                    s["limit_bytes"] = derived
        if "active" in body:
            s["active"] = _as_bool(body["active"])
            deactivated = not s["active"]
            reactivated = bool(s["active"])
        link_ids = list(s.get("link_ids") or [])

    if deactivated:
        # قطع سخت: محلی + نود (remote)
        async with LINKS_LOCK:
            for lid in link_ids:
                if lid in LINKS:
                    LINKS[lid]["active"] = False
            for link in LINKS.values():
                if link.get("sub_id") == sub_id or link.get("multi_group_id") == sub_id:
                    link["active"] = False
        async with NODES_LOCK:
            for lid in link_ids:
                if _is_remote_link_id(lid):
                    _set_remote_active(lid, False)
        log_activity("sub", "اشتراک غیرفعال شد؛ کانفیگ‌های محلی و نود قطع شدند", "warn")
    if reactivated:
        async with LINKS_LOCK:
            for lid in link_ids:
                if lid in LINKS:
                    LINKS[lid]["active"] = True
            for link in LINKS.values():
                if link.get("sub_id") == sub_id or link.get("multi_group_id") == sub_id:
                    link["active"] = True
        async with NODES_LOCK:
            for lid in link_ids:
                if _is_remote_link_id(lid):
                    _set_remote_active(lid, True)
        log_activity("sub", "اشتراک فعال شد و کانفیگ‌هایش روشن شدند", "ok")
    remote_ids = [str(x) for x in link_ids if _is_remote_link_id(str(x))]
    remote_control = {"nodes": 0, "delivered": 0}
    if deactivated or reactivated:
        remote_control = await _control_remote_links(remote_ids, "set_active", bool(reactivated))
    unified_uuid = str(SUBS.get(sub_id, {}).get("unified_uuid") or "")
    if body.get("unify_uuid"):
        unified_uuid = unified_uuid or generate_uuid()
        SUBS[sub_id]["unified_uuid"] = unified_uuid
        remote_control = await _control_remote_links(remote_ids, "set_uuid_alias", unified_uuid)
    elif body.get("unify_uuid") is False:
        SUBS[sub_id]["unified_uuid"] = ""
        unified_uuid = ""
    await save_state()
    return {
        "ok": True,
        "active": SUBS.get(sub_id, {}).get("active", True),
        "membership_changed": membership_changed,
        "unified_uuid": unified_uuid,
        "remote_control": remote_control,
    }

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        name = SUBS[sub_id].get("name", sub_id)
        link_ids = list(SUBS[sub_id].get("link_ids") or [])
        del SUBS[sub_id]
    # حذف اشتراک → محلی + نودهای فقط‌متصل‌به این ساب
    cut = 0
    remote_cut = 0
    async with LINKS_LOCK:
        touched = set(link_ids)
        for lid, link in list(LINKS.items()):
            if (
                lid in touched
                or link.get("sub_id") == sub_id
                or link.get("multi_group_id") == sub_id
            ):
                link["active"] = False
                link["sub_id"] = None
                if link.get("multi_group_id") == sub_id:
                    link["multi_group_id"] = None
                cut += 1
    async with NODES_LOCK:
        # اگر remote فقط در این ساب بود → قطع؛ اگر در ساب دیگری هم هست → بماند
        still_elsewhere = set()
        for sid, s in SUBS.items():
            for lid in s.get("link_ids") or []:
                if _is_remote_link_id(str(lid)):
                    still_elsewhere.add(str(lid))
        for lid in link_ids:
            lid = str(lid)
            if not _is_remote_link_id(lid):
                continue
            if lid in still_elsewhere:
                continue
            if _set_remote_active(lid, False):
                remote_cut += 1
                cut += 1
    await save_state()
    log_activity("sub", f"گروه «{name}» حذف شد و {cut} کانفیگ قطع شد (نود={remote_cut})", "warn")
    return {"ok": True, "deleted": sub_id, "deactivated_links": cut, "remote_cut": remote_cut}

@app.post("/api/subs/{sub_id}/links")
async def assign_link_to_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    link_id = str(body.get("link_id", ""))
    action = str(body.get("action", "add"))
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        ids = s.setdefault("link_ids", [])
        if action == "add":
            if link_id not in ids:
                ids.append(link_id)
            # دیگر از بقیه ساب‌ها حذف نمی‌کنیم (جلوگیری از باگ Me↔Fam)
        else:
            if link_id in ids:
                ids.remove(link_id)
    async with LINKS_LOCK:
        if link_id in LINKS:
            if action == "add":
                if not LINKS[link_id].get("sub_id"):
                    LINKS[link_id]["sub_id"] = sub_id
            elif LINKS[link_id].get("sub_id") == sub_id:
                other = next(
                    (sid for sid, sub in SUBS.items()
                     if sid != sub_id and link_id in (sub.get("link_ids") or [])),
                    None,
                )
                LINKS[link_id]["sub_id"] = other
    await save_state()
    return {"ok": True}


@app.post("/api/links/cut-orphans")
async def cut_orphan_links(_=Depends(require_auth)):
    """قطع کانفیگ‌های محلی و نود که اشتراک والدشان حذف/نامعتبر است."""
    cut_ids = []
    remote_cut = 0
    async with SUBS_LOCK:
        valid_subs = set(SUBS.keys())
        # همه remoteهایی که هنوز در حداقل یک ساب معتبر هستند
        remotes_in_valid = set()
        for sid, s in SUBS.items():
            for lid in s.get("link_ids") or []:
                if _is_remote_link_id(str(lid)):
                    remotes_in_valid.add(str(lid))
        async with LINKS_LOCK:
            for lid, link in LINKS.items():
                sid = link.get("sub_id")
                mid = link.get("multi_group_id")
                orphan = False
                if sid and sid not in valid_subs:
                    orphan = True
                if mid and mid not in valid_subs:
                    orphan = True
                if orphan:
                    link["active"] = False
                    link["sub_id"] = None
                    if mid and mid not in valid_subs:
                        link["multi_group_id"] = None
                    cut_ids.append(lid)
        async with NODES_LOCK:
            # کانفیگ نودی که در هیچ ساب معتبری نیست → غیرفعال
            for node_id, node in NODES.items():
                for idx, cfg in enumerate(node.get("configs") or []):
                    if not isinstance(cfg, dict):
                        continue
                    key = str(cfg.get("source_id") if cfg.get("source_id") not in (None, "") else idx)
                    rid = f"remote:{node_id}:{key}"
                    if rid not in remotes_in_valid and _as_bool(cfg.get("active", True)):
                        cfg["active"] = False
                        remote_cut += 1
                        cut_ids.append(rid)
    await save_state()
    total = len(cut_ids)
    log_activity("system", f"قطع یتیم‌ها: {total} (نود={remote_cut})", "warn")
    return {"ok": True, "cut": total, "remote_cut": remote_cut, "ids": cut_ids}


@app.post("/api/links/cut-inactive-subs")
async def cut_inactive_sub_links(_=Depends(require_auth)):
    """قطع همه کانفیگ‌های محلی و نود متصل به اشتراک‌های غیرفعال + یتیم‌ها."""
    cut_ids = []
    remote_cut = 0
    async with SUBS_LOCK:
        inactive = {sid for sid, s in SUBS.items() if _as_bool(s.get("active", True)) is False}
        valid = set(SUBS.keys())
        # remoteهایی که فقط به ساب‌های غیرفعال وصل‌اند
        remotes_active_sub = set()
        remotes_inactive_sub = set()
        for sid, s in SUBS.items():
            for lid in s.get("link_ids") or []:
                lid = str(lid)
                if not _is_remote_link_id(lid):
                    continue
                if sid in inactive:
                    remotes_inactive_sub.add(lid)
                else:
                    remotes_active_sub.add(lid)
        async with LINKS_LOCK:
            for lid, link in LINKS.items():
                sid = link.get("sub_id")
                mid = link.get("multi_group_id")
                should_cut = False
                if sid and (sid not in valid or sid in inactive):
                    should_cut = True
                if mid and (mid not in valid or mid in inactive):
                    should_cut = True
                if should_cut and _as_bool(link.get("active", True)):
                    link["active"] = False
                    cut_ids.append(lid)
                if sid and sid not in valid:
                    link["sub_id"] = None
                if mid and mid not in valid:
                    link["multi_group_id"] = None
        async with NODES_LOCK:
            for rid in remotes_inactive_sub:
                # اگر هنوز در یک ساب فعال هم هست، قطع نکن
                if rid in remotes_active_sub:
                    continue
                if _set_remote_active(rid, False):
                    remote_cut += 1
                    cut_ids.append(rid)
    await save_state()
    total = len(cut_ids)
    log_activity("system", f"قطع اشتراک‌های غیرفعال: {total} (نود={remote_cut})", "warn")
    return {"ok": True, "cut": total, "remote_cut": remote_cut, "ids": cut_ids}

# ── Public sub-group subscription file ───────────────────────────────────────
@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="not found")
    if sub.get("active", True) is False:
        raise HTTPException(status_code=403, detail="subscription disabled")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")
    host = get_host()
    async with LINKS_LOCK:
        async with NODES_LOCK:
            lines, allowed_links = _collect_sub_share_lines(sub, host)
            info = build_sub_info_lines(allowed_links, sub, host)
            lines = info + lines
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "profile-title": quote(sub["name"]),
            "profile-update-interval": "24",
        }
    )

# ── Auth endpoints ────────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    ip = client_ip(request)
    if not security_client_allowed(ip):
        log_activity("auth", f"ورود از IP غیرمجاز مسدود شد: {ip}", "err")
        raise HTTPException(status_code=403, detail="IP شما مجاز نیست")
    locked, remaining = is_login_locked(ip)
    if locked:
        raise HTTPException(status_code=429, detail=f"ورود موقتاً قفل است؛ {remaining} ثانیه دیگر تلاش کنید")
    if hash_password(str(body.get("password", ""))) != AUTH["password_hash"]:
        record_login_failure(ip)
        log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    record_login_success(ip)
    token = await create_session()
    log_activity("auth", f"ورود موفق به پنل از {ip}", "ok")
    resp = JSONResponse({"ok": True})
    resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
    return resp

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}

@app.post("/api/change-password")
async def api_change_password(request: Request, token=Depends(require_auth)):
    body = await request.json()
    if hash_password(str(body.get("current_password", ""))) != AUTH["password_hash"]:
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        SESSIONS[token] = time.time() + SESSION_TTL
    await save_state()
    log_activity("auth", "رمز عبور پنل تغییر کرد", "ok")
    return {"ok": True}

# ── Stats ─────────────────────────────────────────────────────────────────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": datetime.now().isoformat(),
        "hourly": hourly_last_n(24),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap),
        "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap.values() if is_link_expired(l)),
        "subs_count": len(SUBS),
        "protocol_counts": {
            "vless_ws": sum(1 for l in snap.values() if l.get("protocol") == "vless-ws"),
            "trojan_ws": sum(1 for l in snap.values() if l.get("protocol") == "trojan-ws"),
            "xhttp": sum(1 for l in snap.values() if "xhttp" in str(l.get("protocol", ""))),
            "shadowsocks_tls": sum(1 for l in snap.values() if l.get("protocol") == "shadowsocks-tls"),
            "mtproto": sum(1 for l in snap.values() if l.get("protocol") == "mtproto"),
            "vless_tcp": sum(1 for l in snap.values() if l.get("protocol") == "vless-tcp"),
            "vless_reality": sum(1 for l in snap.values() if l.get("protocol") == "vless-reality"),
        },
        "top_links": sorted([
            {"label": l.get("label", ""), "protocol": l.get("protocol", DEFAULT_PROTOCOL), "used_bytes": l.get("used_bytes", 0)}
            for l in snap.values()
        ], key=lambda x: x["used_bytes"], reverse=True)[:8],
        "db_mode": "JSON File",
    }

@app.get("/api/activity")
async def get_activity(_=Depends(require_auth)):
    return {"logs": list(activity_logs)[-150:]}

def _local_connections_snapshot() -> list[dict]:
    """اتصالات زنده همین پنل — برای گزارش به مرکزی."""
    snap = dict(LINKS)
    grouped: dict[str, dict] = {}
    for conn_id, c in connections.items():
        ip = c.get("ip", "نامشخص")
        link = snap.get(c.get("uuid"))
        label = link.get("label") if link else "نامشخص"
        g = grouped.get(ip)
        if g is None:
            g = {
                "ip": ip,
                "sessions": 0,
                "bytes": 0,
                "labels": set(),
                "transports": set(),
                "first_connected_at": c.get("connected_at"),
                "last_connected_at": c.get("connected_at"),
            }
            grouped[ip] = g
        g["sessions"] += 1
        g["bytes"] += int(c.get("bytes") or 0)
        g["labels"].add(label)
        g["transports"].add(c.get("transport", "vless-ws"))
        ca = c.get("connected_at")
        if ca:
            if not g["first_connected_at"] or ca < g["first_connected_at"]:
                g["first_connected_at"] = ca
            if not g["last_connected_at"] or ca > g["last_connected_at"]:
                g["last_connected_at"] = ca
    try:
        for uid, link in snap.items():
            if link.get("protocol") == "mtproto":
                label = link.get("label", "نامشخص")
                for c in mtproto.get_instance_connections(uid):
                    ip = c["ip"]
                    g = grouped.get(ip)
                    if g is None:
                        g = {
                            "ip": ip, "sessions": 0, "bytes": 0,
                            "labels": set(), "transports": set(),
                            "first_connected_at": None, "last_connected_at": None,
                        }
                        grouped[ip] = g
                    g["sessions"] += 1
                    g["labels"].add(label)
                    g["transports"].add("mtproto")
    except Exception:
        pass
    out = []
    for ip, g in grouped.items():
        out.append({
            "ip": ip,
            "sessions": g["sessions"],
            "labels": sorted(g["labels"]),
            "label": " · ".join(sorted(g["labels"])) if g["labels"] else "نامشخص",
            "transports": sorted(g["transports"]),
            "bytes": g["bytes"],
            "bytes_fmt": fmt_bytes(g["bytes"]),
            "connected_at": g["first_connected_at"],
            "last_connected_at": g["last_connected_at"],
        })
    return out


# ── Live connections (with IP) ────────────────────────────────────────────────
@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    """اتصالات محلی + در نقش مرکزی، اتصالات زنده نودها (pull)."""
    local = _local_connections_snapshot()
    # کلید یکتا: ip + source تا نود و مرکزی قاطی نشوند
    result = []
    for row in local:
        result.append({**row, "source": "local", "node_name": "مرکزی"})

    node_raw = 0
    if _cluster_role() == "central":
        async with NODES_LOCK:
            nodes_snap = [
                {
                    "id": nid,
                    "name": n.get("name") or nid[:8],
                    "host": n.get("host") or "",
                    "token": n.get("token") or "",
                }
                for nid, n in NODES.items()
            ]
        async def _pull_node(ninfo):
            host = (ninfo.get("host") or "").strip()
            token = (ninfo.get("token") or "").strip()
            if not host or not token:
                return 0, []
            base = host if host.startswith("http") else f"https://{host}"
            base = base.rstrip("/")
            out_rows = []
            raw = 0
            try:
                async with httpx.AsyncClient(timeout=3.0, follow_redirects=True) as client:
                    r = await client.get(
                        f"{base}/api/cluster/peer-connections",
                        headers={"X-Node-Token": token, "Authorization": f"Bearer {token}"},
                    )
                    if r.status_code >= 400:
                        return 0, []
                    data = r.json() if r.content else {}
                    rows = data.get("connections") or []
                    raw = int(data.get("raw_count") or len(rows))
                    for row in rows:
                        if not isinstance(row, dict):
                            continue
                        labels = list(row.get("labels") or [])
                        label = row.get("label") or " · ".join(labels) or "نامشخص"
                        out_rows.append({
                            "ip": row.get("ip") or "نامشخص",
                            "sessions": int(row.get("sessions") or 0),
                            "labels": labels,
                            "label": f"[{ninfo['name']}] {label}",
                            "transports": list(row.get("transports") or []),
                            "bytes": int(row.get("bytes") or 0),
                            "bytes_fmt": row.get("bytes_fmt") or fmt_bytes(int(row.get("bytes") or 0)),
                            "connected_at": row.get("connected_at"),
                            "last_connected_at": row.get("last_connected_at"),
                            "source": "node",
                            "node_name": ninfo["name"],
                            "node_id": ninfo["id"],
                        })
            except Exception:
                return 0, []
            return raw, out_rows
        pulled = await asyncio.gather(*[_pull_node(n) for n in nodes_snap])
        for raw, rows in pulled:
            node_raw += int(raw or 0)
            result.extend(rows)

    result.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)
    return {
        "connections": result,
        "count": len(result),
        "raw_count": len(connections) + node_raw,
        "local_count": len(local),
        "node_count": max(0, len(result) - len(local)),
    }


@app.get("/api/cluster/peer-connections")
async def api_cluster_peer_connections(request: Request):
    """نود: اتصالات زنده را با node_token به مرکزی می‌دهد (بدون session ادمین)."""
    if _cluster_role() != "node":
        # روی مرکزی هم می‌توان local برگرداند اگر token نود نبود
        node = _verify_node_token(request)
        if not node:
            raise HTTPException(status_code=401, detail="node token نامعتبر است")
    else:
        c = _cluster()
        token = (
            request.headers.get("X-Node-Token")
            or (request.headers.get("Authorization") or "").replace("Bearer", "").strip()
        )
        if not token or token != (c.get("node_token") or ""):
            raise HTTPException(status_code=401, detail="node token نامعتبر است")
    rows = _local_connections_snapshot()
    return {
        "ok": True,
        "connections": rows,
        "count": len(rows),
        "raw_count": len(connections),
        "role": _cluster_role(),
        "host": get_host(),
    }


# ── Cloudflare Domains / Clean IP subscriptions ─────────────────────────────
def _cf_domains() -> list[dict]:
    cf = SETTINGS.setdefault("cloudflare", {"domains": []})
    if isinstance(cf, dict):
        cf.setdefault("domains", [])
        return cf["domains"]
    SETTINGS["cloudflare"] = {"domains": []}
    return SETTINGS["cloudflare"]["domains"]

def _norm_domain(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://", "", value).split("/", 1)[0].strip().strip(".")
    return value

def _norm_clean_ips(raw) -> list[str]:
    # Supports IPv4, domains, and IPv6 literals. Backslash-escaped colons from chat copy are normalized.
    parts = re.split(r"[\n,\s]+", raw) if isinstance(raw, str) else list(raw or [])
    out=[]
    for x in parts:
        x=str(x).strip().replace("\\:", ":")
        if x.startswith("[") and x.endswith("]"):
            x=x[1:-1].strip()
        if x and x not in out:
            out.append(x)
    return out[:300]

def _cf_slug(domain: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", domain).strip("-") or secrets.token_urlsafe(8)

def _find_cf_domain(key: str) -> dict | None:
    key = _norm_domain(key) or key
    for d in _cf_domains():
        if d.get("domain") == key or d.get("slug") == key:
            return d
    return None


def _extra_domains() -> list[dict]:
    items = SETTINGS.setdefault("extra_domains", [])
    if not isinstance(items, list):
        SETTINGS["extra_domains"] = []
        return SETTINGS["extra_domains"]
    return items

def _find_extra_domain(key: str) -> dict | None:
    key_n = _norm_domain(key) or key
    for d in _extra_domains():
        if d.get("domain") == key_n or d.get("slug") == key or d.get("id") == key:
            return d
    return None


def _config_ports_for_proto(proto: str) -> tuple[int, ...]:
    """HTTPS 443 + HTTP 80 for all tunnel protocols (not MTProto)."""
    if proto == "mtproto":
        return ()
    return (443, 80)

def _share_lines_for_all_domains(uid: str, link: dict, host: str, sub: dict | None = None) -> list[str]:
    """کانفیگ‌های یک لینک برای دامنه اصلی + کلادفلیر + دامنه‌های فرعی — با پورت 443 (HTTPS)."""
    proto = link.get("protocol", DEFAULT_PROTOCOL)
    lines: list[str] = []
    if proto == "mtproto":
        remark = format_config_remark(link, target=host, domain=host, sub=sub, cdn=False)
        lines.append(generate_share_link(uid, host, remark=remark, protocol=proto))
        return lines
    remark = format_config_remark(link, target=host, domain=host, sub=sub, cdn=False)
    lines.append(generate_share_link(uid, host, remark=remark, protocol=proto))
    # دامنه‌های Cloudflare (با IP تمیز یا خود دامنه)
    for cf in _cf_domains():
        domain = cf.get("domain") or ""
        if not domain:
            continue
        clean_ips = cf.get("clean_ips") or []
        targets = clean_ips if clean_ips else [domain]
        for target in targets:
            cdn_name = str(cf.get("name") or domain)
            remark = format_config_remark(
                link, target=str(target), domain=domain, sub=sub, cdn=True,
                cdn_name=cdn_name, extra_name=cdn_name,
            )
            lines.append(generate_share_link(uid, target, remark=remark, protocol=proto, sni_host=domain))
    # دامنه‌های فرعی (+ IP/دامنه تمیز مثل کلادفلیر)
    for ed in _extra_domains():
        domain = ed.get("domain") or ""
        if not domain:
            continue
        clean_ips = ed.get("clean_ips") or []
        targets = clean_ips if clean_ips else [domain]
        extra_name = str(ed.get("name") or domain)
        for target in targets:
            remark = format_config_remark(
                link, target=str(target), domain=domain, sub=sub, cdn=False,
                cdn_name=extra_name, extra_name=extra_name,
            )
            lines.append(generate_share_link(uid, target, remark=remark, protocol=proto, sni_host=domain))
    return lines

def domain_sub_urls_for_key(host: str, uuid_key: str) -> dict:
    """URLهای ساب جدا برای دامنه اصلی و دامنه‌های فرعی."""
    main_url = f"https://{host}/domain-sub/main/{uuid_key}"
    extra = []
    for ed in _extra_domains():
        slug = ed.get("slug") or _cf_slug(ed.get("domain", ""))
        extra.append({
            "name": ed.get("name") or ed.get("domain"),
            "domain": ed.get("domain"),
            "slug": slug,
            "sub_url": f"https://{host}/domain-sub/extra/{slug}/{uuid_key}",
        })
    return {"main_domain": host, "main_sub_url": main_url, "extra_subs": extra}

def cloudflare_sub_urls_for_key(host: str, uuid_key: str) -> list[dict]:
    return [
        {
            "name": cf.get("name") or cf.get("domain"),
            "domain": cf.get("domain"),
            "slug": cf.get("slug") or _cf_slug(cf.get("domain", "")),
            "clean_ip_count": len(cf.get("clean_ips") or []),
            "sub_url": f"https://{host}/cf-sub/{cf.get('slug') or _cf_slug(cf.get('domain',''))}/{uuid_key}",
        }
        for cf in _cf_domains()
    ]

@app.get("/api/cloudflare/domains")
async def api_cloudflare_domains(_=Depends(require_auth)):
    host=get_host()
    items=[]
    for d in _cf_domains():
        slug=d.get('slug') or _cf_slug(d.get('domain',''))
        items.append({**d, "slug": slug, "sub_url": f"https://{host}/cf-sub/{slug}", "group_sub_template": f"https://{host}/cf-sub/{slug}/{{uuid_key}}"})
    return {"domains": items}

@app.post("/api/cloudflare/domains")
async def api_cloudflare_save_domain(request: Request, _=Depends(require_auth)):
    body = await request.json()
    domain = _norm_domain(body.get("domain") or "")
    if not domain or "." not in domain:
        raise HTTPException(status_code=400, detail="دامنه کلادفلیر معتبر نیست")
    clean_ips = _norm_clean_ips(body.get("clean_ips") or body.get("ips") or "")
    name = (body.get("name") or domain).strip()[:80]
    key = str(body.get("key") or body.get("id") or body.get("slug") or "").strip()
    domains = _cf_domains()
    item = next((x for x in domains if key and (x.get("id") == key or x.get("slug") == key or x.get("domain") == _norm_domain(key))), None)
    if not item:
        item = next((x for x in domains if x.get("domain") == domain), None)
    if not item:
        item = {"id": generate_uuid(), "slug": _cf_slug(domain), "domain": domain, "created_at": datetime.now().isoformat()}
        domains.append(item)
    old_slug = item.get("slug")
    item.update({"name": name, "domain": domain, "slug": _cf_slug(domain), "clean_ips": clean_ips, "updated_at": datetime.now().isoformat()})
    if old_slug and old_slug != item["slug"]:
        item["previous_slug"] = old_slug
    await save_state()
    host=get_host()
    return {"ok": True, "domain": item, "sub_url": f"https://{host}/cf-sub/{item['slug']}"}

@app.delete("/api/cloudflare/domains/{key}")
async def api_cloudflare_delete_domain(key: str, _=Depends(require_auth)):
    domains=_cf_domains(); item=_find_cf_domain(key)
    if not item:
        raise HTTPException(status_code=404, detail="دامنه پیدا نشد")
    domains.remove(item)
    await save_state()
    return {"ok": True}

@app.get("/cf-sub/{key}")
async def cloudflare_subscription(key: str):
    import base64
    item=_find_cf_domain(key)
    if not item:
        raise HTTPException(status_code=404, detail="cloudflare domain not found")
    domain=item.get("domain")
    clean_ips=item.get("clean_ips") or []
    targets=clean_ips if clean_ips else [domain]
    async with LINKS_LOCK:
        snap=dict(LINKS)
    lines=[]
    for uid, link in snap.items():
        if not is_link_allowed(link):
            continue
        proto=link.get("protocol", DEFAULT_PROTOCOL)
        if proto == "mtproto":
            continue
        for target in targets:
            remark = format_config_remark(
                link, target=str(target), domain=domain, cdn=True,
                cdn_name=str(item.get("name") or domain), extra_name=str(item.get("name") or domain),
            )
            lines.append(generate_share_link(uid, target, remark=remark, protocol=proto, sni_host=domain))
    content=base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={"profile-title": quote(f"OXNET Cloudflare {domain}")})


@app.get("/cf-sub/{key}/{uuid_key}")
async def cloudflare_group_subscription(key: str, uuid_key: str, request: Request):
    import base64
    item=_find_cf_domain(key)
    if not item:
        raise HTTPException(status_code=404, detail="cloudflare domain not found")
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="sub not found")
    if sub.get("active", True) is False:
        raise HTTPException(status_code=403, detail="subscription disabled")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")
    domain=item.get("domain")
    clean_ips=item.get("clean_ips") or []
    targets=clean_ips if clean_ips else [domain]
    link_ids=sub.get("link_ids", [])
    async with LINKS_LOCK:
        async with NODES_LOCK:
            allowed=[]
            lines=[]
            for lid in link_ids:
                lid=str(lid)
                if _is_remote_link_id(lid):
                    cfg=_resolve_remote_config(lid)
                    if cfg and cfg.get("active") and cfg.get("uri"):
                        # URI نود دست‌نخورده می‌ماند (host/UUID خود نود)
                        lines.append(cfg["uri"])
                        allowed.append({"label": cfg.get("label"), "used_bytes": 0, "limit_bytes": 0, "active": True})
                    continue
                link=LINKS.get(lid)
                if not link or not is_link_allowed(link):
                    continue
                allowed.append(link)
                proto=link.get("protocol", DEFAULT_PROTOCOL)
                if proto == "mtproto":
                    continue
                for target in targets:
                    remark=format_config_remark(
                        link, target=str(target), domain=domain, sub=sub, cdn=True,
                        cdn_name=str(item.get("name") or domain), extra_name=str(item.get("name") or domain),
                    )
                    lines.append(generate_share_link(lid, target, remark=remark, protocol=proto, sni_host=domain))
            lines = list(dict.fromkeys(lines))
            lines = build_sub_info_lines(allowed, sub, get_host()) + lines
    content=base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={"profile-title": quote(f"{sub.get('name','OXNET')} Cloudflare {domain}")})


# ── Extra domains (دامنه فرعی) + domain-specific subs ─────────────────────────
@app.get("/api/extra-domains")
async def api_extra_domains(_=Depends(require_auth)):
    host = get_host()
    items = []
    for d in _extra_domains():
        slug = d.get("slug") or _cf_slug(d.get("domain", ""))
        items.append({
            **d,
            "slug": slug,
            "sub_url": f"https://{host}/domain-sub/extra/{slug}",
            "group_sub_template": f"https://{host}/domain-sub/extra/{slug}/{{uuid_key}}",
        })
    return {"domains": items, "panel_domain": host}

@app.post("/api/extra-domains")
async def api_extra_domain_save(request: Request, _=Depends(require_auth)):
    body = await request.json()
    domain = _norm_domain(body.get("domain") or "")
    if not domain or "." not in domain:
        raise HTTPException(status_code=400, detail="دامنه فرعی معتبر نیست")
    name = (body.get("name") or domain).strip()[:80]
    clean_ips = _norm_clean_ips(body.get("clean_ips") or body.get("ips") or "")
    key = str(body.get("key") or body.get("id") or body.get("slug") or "").strip()
    domains = _extra_domains()
    item = next((x for x in domains if key and (x.get("id") == key or x.get("slug") == key or x.get("domain") == _norm_domain(key))), None)
    if not item:
        item = next((x for x in domains if x.get("domain") == domain), None)
    if not item:
        item = {"id": generate_uuid(), "slug": _cf_slug(domain), "domain": domain, "created_at": datetime.now().isoformat(), "clean_ips": []}
        domains.append(item)
    item.update({
        "name": name,
        "domain": domain,
        "slug": _cf_slug(domain),
        "clean_ips": clean_ips,
        "updated_at": datetime.now().isoformat(),
    })
    await save_state()
    host = get_host()
    return {"ok": True, "domain": item, "sub_url": f"https://{host}/domain-sub/extra/{item['slug']}"}

@app.delete("/api/extra-domains/{key}")
async def api_extra_domain_delete(key: str, _=Depends(require_auth)):
    domains = _extra_domains()
    item = _find_extra_domain(key)
    if not item:
        raise HTTPException(status_code=404, detail="دامنه فرعی پیدا نشد")
    domains.remove(item)
    await save_state()
    return {"ok": True}

@app.get("/domain-sub/main/{uuid_key}")
async def domain_sub_main(uuid_key: str, request: Request):
    """ساب فقط با دامنه اصلی پنل."""
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="not found")
    if sub.get("active", True) is False:
        raise HTTPException(status_code=403, detail="subscription disabled")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")
    host = get_host()
    async with LINKS_LOCK:
        async with NODES_LOCK:
            lines, allowed = _collect_sub_share_lines(sub, host)
            lines = build_sub_info_lines(allowed, sub, host) + lines
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={
        "profile-title": quote(f"{sub.get('name','OXNET')} Main"),
        "profile-update-interval": "24",
    })

@app.get("/domain-sub/extra/{key}")
async def domain_sub_extra_all(key: str):
    """ساب همه کانفیگ‌های فعال فقط روی یک دامنه فرعی (+ clean IP)."""
    import base64
    item = _find_extra_domain(key)
    if not item:
        raise HTTPException(status_code=404, detail="extra domain not found")
    domain = item.get("domain")
    clean_ips = item.get("clean_ips") or []
    targets = clean_ips if clean_ips else [domain]
    host = get_host()
    async with LINKS_LOCK:
        snap = dict(LINKS)
    lines = []
    for uid, link in snap.items():
        if not is_link_allowed(link):
            continue
        proto = link.get("protocol", DEFAULT_PROTOCOL)
        if proto == "mtproto":
            continue
        for target in targets:
            remark = format_config_remark(
                link, target=str(target), domain=domain, cdn=False,
                cdn_name=str(item.get("name") or domain), extra_name=str(item.get("name") or domain),
            )
            lines.append(generate_share_link(uid, target, remark=remark, protocol=proto, sni_host=domain))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={"profile-title": quote(f"OXNET {domain}")})

@app.get("/domain-sub/extra/{key}/{uuid_key}")
async def domain_sub_extra_group(key: str, uuid_key: str, request: Request):
    import base64
    item = _find_extra_domain(key)
    if not item:
        raise HTTPException(status_code=404, detail="extra domain not found")
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="sub not found")
    if sub.get("active", True) is False:
        raise HTTPException(status_code=403, detail="subscription disabled")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")
    domain = item.get("domain")
    clean_ips = item.get("clean_ips") or []
    targets = clean_ips if clean_ips else [domain]
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        async with NODES_LOCK:
            allowed = []
            lines = []
            for lid in link_ids:
                lid = str(lid)
                if _is_remote_link_id(lid):
                    cfg = _resolve_remote_config(lid)
                    if cfg and cfg.get("active") and cfg.get("uri"):
                        lines.append(cfg["uri"])
                        allowed.append({"label": cfg.get("label"), "used_bytes": 0, "limit_bytes": 0, "active": True})
                    continue
                link = LINKS.get(lid)
                if not link or not is_link_allowed(link):
                    continue
                allowed.append(link)
                proto = link.get("protocol", DEFAULT_PROTOCOL)
                if proto == "mtproto":
                    continue
                for target in targets:
                    remark = format_config_remark(
                        link, target=str(target), domain=domain, sub=sub, cdn=False,
                        cdn_name=str(item.get("name") or domain), extra_name=str(item.get("name") or domain),
                    )
                    lines.append(generate_share_link(lid, target, remark=remark, protocol=proto, sni_host=domain))
            lines = list(dict.fromkeys(lines))
            lines = build_sub_info_lines(allowed, sub, get_host()) + lines
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={
        "profile-title": quote(f"{sub.get('name','OXNET')} {domain}"),
        "profile-update-interval": "24",
    })

# ── Link Management ───────────────────────────────────────────────────────────
@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    label = (body.get("label") or "لینک جدید").strip()[:60]
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    note = (body.get("note") or "").strip()[:200]
    sub_id = body.get("sub_id") or None
    protocol = body.get("protocol") or DEFAULT_PROTOCOL
    if protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL
    custom_path = normalize_config_path(body.get("custom_path"))

    if protocol == "multi":
        host = get_host()
        base_path = await unique_config_path(custom_path, generate_uuid()[:8])
        sub_id = generate_uuid()
        uuid_key = base_path
        multi_protocols = [
            "vless-ws", "xhttp-packet-up", "xhttp-stream-up",
            "trojan-ws", "trojan-xhttp-packet-up", "trojan-xhttp-stream-up",
            "shadowsocks-tls",
        ]
        # Include Railway TCP / Reality in multi only when settings are filled
        tcp = SETTINGS.get("railway_tcp") or {}
        if tcp.get("domain") and int(tcp.get("port") or 0) > 0:
            multi_protocols.append("vless-tcp")
        real = SETTINGS.get("reality") or {}
        if real.get("host") and real.get("pbk"):
            multi_protocols.append("vless-reality")
        sub = {
            "name": label,
            "desc": "Multi Protocol subscription",
            "uuid_key": uuid_key,
            "password_hash": None,
            "created_at": datetime.now().isoformat(),
            "link_ids": [],
        }
        links_out = []
        async with LINKS_LOCK:
            for p in multi_protocols:
                muid = generate_uuid()
                mpath = secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:9]
                i = 2
                used_paths = {str(v.get('path')) for v in LINKS.values() if v.get('path')}
                while mpath in LINKS or mpath in used_paths:
                    mpath = f"{base_path}-{proto_slug(p)}-{i}"
                    i += 1
                LINKS[muid] = {
                    "label": f"{label} - {p}",
                    "limit_bytes": limit_bytes,
                    "used_bytes": 0,
                    "created_at": datetime.now().isoformat(),
                    "active": True,
                    "expires_at": expires_at,
                    "note": note,
                    "is_default": False,
                    "sub_id": sub_id,
                    "protocol": p,
                    "path": mpath,
                    "is_multi_child": True,
                    "multi_group_id": sub_id,
                    "multi_group_path": base_path,
                    "ad_tag": None,
                    "sync_to_central": True,
                }
                sub["link_ids"].append(muid)
                links_out.append({"uuid": muid, "path": mpath, "protocol": p, "vless_link": generate_share_link(muid, host, remark=f"{label}-{p}", protocol=p)})
        async with SUBS_LOCK:
            SUBS[sub_id] = sub
        await save_state()
        log_activity("link", f"ساب مولتی پروتکل «{label}» ساخته شد", "ok")
        return {"ok": True, "mode": "multi", "sub_id": sub_id, "path": uuid_key, "sub_url": f"https://{host}/sub-group/{uuid_key}", "links": links_out}

    uid = generate_uuid()
    public_path = await unique_config_path(custom_path, uid)
    link_data = {
        "label": label,
        "limit_bytes": limit_bytes,
        "used_bytes": 0,
        "created_at": datetime.now().isoformat(),
        "active": True,
        "expires_at": expires_at,
        "note": note,
        "is_default": False,
        "sub_id": sub_id,
        "protocol": protocol,
        "path": public_path,
        "ad_tag": None,
        "sync_to_central": _as_bool(body.get("sync_to_central", True)),
    }

    if protocol == "mtproto":
        raw_port = body.get("mtproto_port")
        manual_port = int(raw_port) if raw_port not in (None, "", 0, "0") else None
        if manual_port is not None and not (1 <= manual_port <= 65535):
            raise HTTPException(status_code=400, detail="شماره پورت نامعتبر است")
        raw_domain = (body.get("mtproto_domain") or "").strip()
        domain = raw_domain if raw_domain else mtproto.DEFAULT_FAKE_TLS_DOMAIN
        try:
            inst = await mtproto.start_instance(
                uid,
                domain=domain,
                preferred_port=manual_port,
                force_port=manual_port is not None,
                ad_tag=None,
            )
        except RuntimeError as exc:
            logger.error(f"راه‌اندازی MTProto ناموفق برای {uid[:8]}: {exc}")
            raise HTTPException(status_code=409, detail=str(exc))
        except Exception as exc:
            logger.error(f"راه‌اندازی MTProto ناموفق برای {uid[:8]}: {exc}")
            raise HTTPException(status_code=502, detail=f"راه‌اندازی MTProto ناموفق: {exc}")
        link_data["mtproto_port"] = inst["port"]
        link_data["mtproto_secret"] = inst["secret"]
        link_data["mtproto_domain"] = inst["domain"]
        link_data["mtproto_manual_port"] = manual_port is not None
        link_data["mtproto_public_pending"] = False

    # Optional per-link overrides for Railway TCP / Reality (fallback to SETTINGS)
    if protocol == "vless-tcp":
        if body.get("tcp_domain"):
            link_data["tcp_domain"] = re.sub(r"^https?://", "", str(body.get("tcp_domain")).strip(), flags=re.I).split("/", 1)[0].strip()
        if body.get("tcp_port") not in (None, "", 0, "0"):
            try:
                p = int(body.get("tcp_port"))
                if 1 <= p <= 65535:
                    link_data["tcp_port"] = p
            except (TypeError, ValueError):
                pass
        if body.get("tcp_path_mode") in ("panel", "root"):
            link_data["tcp_path_mode"] = body.get("tcp_path_mode")
        tcp = SETTINGS.get("railway_tcp") or {}
        if not (link_data.get("tcp_domain") or tcp.get("domain")):
            raise HTTPException(status_code=400, detail="دامنه TCP Proxy در تنظیمات یا هنگام ساخت کانفیگ الزامی است")
        if not (link_data.get("tcp_port") or tcp.get("port")):
            raise HTTPException(status_code=400, detail="پورت TCP Proxy در تنظیمات یا هنگام ساخت کانفیگ الزامی است")

    if protocol == "vless-reality":
        for key in ("reality_host", "reality_pbk", "reality_sid", "reality_sni", "reality_fp", "reality_spx"):
            if body.get(key):
                link_data[key] = str(body.get(key)).strip()
        if body.get("reality_port") not in (None, "", 0, "0"):
            try:
                p = int(body.get("reality_port"))
                if 1 <= p <= 65535:
                    link_data["reality_port"] = p
            except (TypeError, ValueError):
                pass
        r = SETTINGS.get("reality") or {}
        host_ok = link_data.get("reality_host") or r.get("host")
        pbk_ok = link_data.get("reality_pbk") or r.get("pbk")
        if not host_ok:
            raise HTTPException(status_code=400, detail="Host/IP Reality در تنظیمات یا هنگام ساخت کانفیگ الزامی است")
        if not pbk_ok:
            raise HTTPException(status_code=400, detail="Public Key (pbk) Reality در تنظیمات یا هنگام ساخت کانفیگ الزامی است")

    async with LINKS_LOCK:
        LINKS[uid] = link_data

    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    await save_state()
    log_activity("link", f"کانفیگ «{label}» ساخته شد", "ok")
    host = get_host()
    return {
        "uuid": uid,
        **LINKS[uid],
        "expired": False,
        "vless_link": generate_share_link(uid, host, remark=f"{label}", protocol=protocol),
        "sub_url": f"https://{host}/sub/{LINKS[uid].get('path') or uid}",
    }

@app.get("/api/links")
async def list_links(_=Depends(require_auth)):
    host = get_host()
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for uid, d in snap.items():
        proto = d.get("protocol", DEFAULT_PROTOCOL)
        result.append({
            "uuid": uid,
            **d,
            "protocol": proto,
            "active": _as_bool(d.get("active", True)),
            "allowed": is_link_allowed(d),
            "expired": is_link_expired(d),
            "vless_link": generate_share_link(uid, host, remark=f"{d['label']}", protocol=proto),
            "sub_url": f"https://{host}/sub/{d.get('path') or uid}",
        })
    if _cluster_role() == "central":
        async with NODES_LOCK:
            for node_id, node in NODES.items():
                for idx, cfg in enumerate(node.get("configs") or []):
                    if not isinstance(cfg, dict):
                        continue
                    uri = str(cfg.get("uri") or "").strip()
                    if not uri:
                        continue
                    result.append({
                        "uuid": f"remote:{node_id}:{cfg.get('source_id') or idx}",
                        "label": cfg.get("label") or "Node config",
                        "protocol": cfg.get("protocol") or "remote",
                        "active": _as_bool(cfg.get("active", True)),
                        "allowed": _as_bool(cfg.get("active", True)),
                        "expired": False,
                        "used_bytes": int(cfg.get("used_bytes") or 0),
                        "limit_bytes": 0,
                        "created_at": node.get("last_seen") or node.get("created_at") or datetime.now().isoformat(),
                        "vless_link": uri,
                        "sub_url": "",
                        "remote_node": True,
                        "node_id": node_id,
                        "node_name": node.get("name") or "Node",
                        "node_region": node.get("region") or "",
                        "domain_kind": cfg.get("domain_kind") or "",
                        "target": cfg.get("target") or "",
                        "sync_to_central": True,
                        "remote_group_ids": cfg.get("group_ids") or [],
                        "remote_group_names": cfg.get("group_names") or [],
                        "canonical_uuid": cfg.get("canonical_uuid") or "",
                    })
    result.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    # کانفیگ نود (remote:…) — فقط active/label روی NODES
    if _is_remote_link_id(uid):
        async with NODES_LOCK:
            if "active" in body:
                ok = _set_remote_active(uid, _as_bool(body["active"]))
                if not ok:
                    raise HTTPException(status_code=404, detail="remote link not found")
                log_activity(
                    "link",
                    f"کانفیگ نود «{uid}» {'فعال' if _as_bool(body['active']) else 'غیرفعال'} شد",
                    "ok" if _as_bool(body["active"]) else "warn",
                )
            if "label" in body:
                parts = str(uid).split(":", 2)
                if len(parts) >= 3:
                    node = NODES.get(parts[1])
                    src = parts[2]
                    if node:
                        for idx, cfg in enumerate(node.get("configs") or []):
                            if not isinstance(cfg, dict):
                                continue
                            key = str(cfg.get("source_id") if cfg.get("source_id") not in (None, "") else idx)
                            if key == src:
                                cfg["label"] = str(body["label"])[:100]
                                break
        await save_state()
        return {"ok": True, "remote": True}

    mtproto_action = None
    new_sub = "UNCHANGED"
    resolved = await resolve_link_id(uid) or uid
    reactivate_sub_id = None

    async with LINKS_LOCK:
        if resolved not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        uid = resolved
        link = LINKS[uid]
        old_sub = link.get("sub_id")
        label = link.get("label")

        if "active" in body:
            new_active = _as_bool(body["active"])
            changed = new_active != _as_bool(link.get("active", True))
            link["active"] = bool(new_active)
            log_activity("link", f"کانفیگ «{label}» {'فعال' if new_active else 'غیرفعال'} شد", "ok" if new_active else "warn")
            # اگر لینک فعال شد ولی ساب والد غیرفعال است → ساب را هم روشن کن
            if new_active and link.get("sub_id"):
                sid = link.get("sub_id")
                if sid in SUBS:
                    reactivate_sub_id = sid
                else:
                    # ساب حذف شده — وابستگی را قطع کن تا کانفیگ دوباره کار کند
                    link["sub_id"] = None
            if changed and link.get("protocol") == "mtproto":
                mtproto_action = ("start" if new_active else "stop", dict(link))
        if "label" in body:
            link["label"] = str(body["label"])[:60]
        if "note" in body:
            link["note"] = str(body["note"])[:200]
        if "sync_to_central" in body:
            link["sync_to_central"] = _as_bool(body.get("sync_to_central"))
            log_activity("system", f"ارسال کانفیگ «{link.get('label', label)}» به مرکزی {'فعال' if link['sync_to_central'] else 'غیرفعال'} شد", "info")
        if "reset_usage" in body and body["reset_usage"]:
            link["used_bytes"] = 0
            log_activity("link", f"مصرف کانفیگ «{label}» ریست شد", "info")
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if any(k in body for k in ("label", "note", "limit_value", "expires_days")):
            log_activity("link", f"کانفیگ «{link['label']}» ویرایش شد", "info")
        new_sub = body.get("sub_id", "UNCHANGED")
        if new_sub != "UNCHANGED":
            link["sub_id"] = new_sub or None

    if new_sub != "UNCHANGED":
        async with SUBS_LOCK:
            if old_sub and old_sub in SUBS:
                ids = SUBS[old_sub].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
            if new_sub and new_sub in SUBS:
                ids = SUBS[new_sub].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    # فعال‌سازی دستی کانفیگ → ساب والد هم فعال شود تا is_link_allowed قطع نکند
    if reactivate_sub_id:
        async with SUBS_LOCK:
            if reactivate_sub_id in SUBS:
                SUBS[reactivate_sub_id]["active"] = True

    if mtproto_action:
        action, snap = mtproto_action
        if action == "stop":
            await mtproto.stop_instance(uid)
        else:
            try:
                old_port = snap.get("mtproto_port")
                inst = await mtproto.start_instance(
                    uid,
                    secret=snap.get("mtproto_secret"),
                    domain=snap.get("mtproto_domain", mtproto.DEFAULT_FAKE_TLS_DOMAIN),
                    preferred_port=snap.get("mtproto_port"),
                    force_port=snap.get("mtproto_manual_port", False),
                    ad_tag=snap.get("ad_tag"),
                )
                async with LINKS_LOCK:
                    if uid in LINKS:
                        LINKS[uid]["mtproto_port"] = inst["port"]
                        LINKS[uid]["mtproto_secret"] = inst["secret"]
                if (snap.get("mtproto_proxy_id") and inst["port"] != old_port
                        and not snap.get("mtproto_manual_port", False)):
                    asyncio.create_task(_reattach_mtproto_public_proxy(
                        uid, inst["port"], snap.get("mtproto_proxy_id"), snap.get("label", "")
                    ))
            except Exception as exc:
                logger.error(f"روشن کردن MTProto ناموفق برای {uid[:8]}: {exc}")
                async with LINKS_LOCK:
                    if uid in LINKS:
                        LINKS[uid]["active"] = False
                log_activity("link", f"روشن کردن پروکسی تلگرام «{label}» ناموفق بود", "err")
                await save_state()
                raise HTTPException(status_code=502, detail=f"روشن کردن پروکسی تلگرام ناموفق بود: {exc}")

    await save_state()
    return {"ok": True}

# ===== Endpoint جدید برای به‌روزرسانی ad_tag =====
@app.patch("/api/links/{uid}/ad-tag")
async def update_ad_tag(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    ad_tag = str(body.get("ad_tag", "")).strip()
    if not ad_tag:
        raise HTTPException(status_code=400, detail="ad_tag نمی‌تواند خالی باشد")

    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        if link.get("protocol") != "mtproto":
            raise HTTPException(status_code=400, detail="این کانفیگ MTProto نیست")
        link["ad_tag_status"] = "pending"   # ← جدید

    asyncio.create_task(_update_mtproto_ad_tag(uid, ad_tag))
    log_activity("link", f"درخواست به‌روزرسانی ad_tag برای «{link.get('label','')}» ثبت شد", "info")
    return {"ok": True, "message": "ad_tag در حال اعمال است، پروکسی ری‌استارت می‌شود"}


# اندپوینت جدید برای پول کردن وضعیت
@app.get("/api/links/{uid}/ad-tag/status")
async def get_ad_tag_status(uid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if not link:
            raise HTTPException(status_code=404, detail="link not found")
        return {
            "status": link.get("ad_tag_status", "idle"),
            "link": link.get("ad_tag_link"),
            "ad_tag": link.get("ad_tag"),
        }

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    # حذف کانفیگ نود از لیست مرکزی (+ از link_ids ساب‌ها)
    if _is_remote_link_id(uid):
        parts = str(uid).split(":", 2)
        label = uid
        async with NODES_LOCK:
            if len(parts) >= 3:
                node = NODES.get(parts[1])
                src = parts[2]
                if node:
                    keep = []
                    for idx, cfg in enumerate(node.get("configs") or []):
                        if not isinstance(cfg, dict):
                            continue
                        key = str(cfg.get("source_id") if cfg.get("source_id") not in (None, "") else idx)
                        if key == src:
                            label = cfg.get("label") or uid
                            continue
                        keep.append(cfg)
                    node["configs"] = keep
        async with SUBS_LOCK:
            for s in SUBS.values():
                ids = s.get("link_ids") or []
                if uid in ids:
                    s["link_ids"] = [x for x in ids if x != uid]
        await save_state()
        log_activity("link", f"کانفیگ نود «{label}» از مرکزی حذف شد", "err")
        return {"ok": True, "deleted": uid, "remote": True}

    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        label = LINKS[uid].get("label", uid)
        sub_id = LINKS[uid].get("sub_id")
        proto = LINKS[uid].get("protocol")
        del LINKS[uid]
    if proto == "mtproto":
        await mtproto.stop_instance(uid)
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    await save_state()
    log_activity("link", f"کانفیگ «{label}» حذف شد", "err")
    return {"ok": True, "deleted": uid}

# ══════════════════════════════════════════════════════════════════════════════
# VLESS Relay
# ══════════════════════════════════════════════════════════════════════════════
from relay_vless import (
    RELAY_BUF,
    parse_vless_header,
    check_and_use,
    relay_ws_to_tcp,
    relay_tcp_to_ws,
    websocket_tunnel,
)

from trojan import trojan_ws_tunnel
from shadowsocks_ws import shadowsocks_ws_tunnel

app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)
app.add_api_websocket_route("/trojan-ws", trojan_ws_tunnel)
app.add_api_websocket_route("/ss/{uuid}", shadowsocks_ws_tunnel)

# ══════════════════════════════════════════════════════════════════════════════
# XHTTP
# ══════════════════════════════════════════════════════════════════════════════
from xhttp_siz10 import router as xhttp_router
app.include_router(xhttp_router)

# ── HTTP Proxy ────────────────────────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization",
        "te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        resp = await http_client.request(method=request.method, url=target_url, headers=headers, content=body)
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        bump_hourly(len(resp.content))
        return Response(content=resp.content, status_code=resp.status_code,
                        headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")

# ── Public sub page ───────────────────────────────────────────────────────────
@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    from pages import get_public_page_html
    async with SUBS_LOCK:
        sub = next(({"sub_id": sid, **s} for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px'>گروه پیدا نشد</h2>", status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub_entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="not found")
    sub_id, sub = sub_entry

    has_pw = sub.get("password_hash") is not None
    if has_pw:
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})

    host = get_host()
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        snap = dict(LINKS)

    links_out = []
    active_conns = 0
    for lid in link_ids:
        link = snap.get(lid)
        if not link:
            continue
        allowed = is_link_allowed(link)
        conn_count = sum(1 for c in connections.values() if c.get("uuid") == lid)
        active_conns += conn_count
        proto = link.get("protocol", DEFAULT_PROTOCOL)
        links_out.append({
            "uuid": lid,
            "label": link["label"],
            "active": allowed,
            "protocol": proto,
            "used_bytes": link.get("used_bytes", 0),
            "used_fmt": fmt_bytes(link.get("used_bytes", 0)),
            "limit_bytes": link.get("limit_bytes", 0),
            "limit_fmt": "∞" if link.get("limit_bytes", 0) == 0 else fmt_bytes(link["limit_bytes"]),
            "expires_at": link.get("expires_at"),
            "vless_link": generate_share_link(lid, host, remark=f"{link['label']}", protocol=proto),
            "sub_url": f"https://{host}/sub/{link.get('path') or lid}",
            "connections": conn_count,
        })

    total_used = sum(l["used_bytes"] for l in links_out)
    return {
        "locked": False,
        "name": sub["name"],
        "desc": sub.get("desc", ""),
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
        "cloudflare_subs": cloudflare_sub_urls_for_key(host, uuid_key),
        "domain_subs": domain_sub_urls_for_key(host, uuid_key),
        "active_connections": active_conns,
        "total_used_fmt": fmt_bytes(total_used),
        "links": links_out,
    }


# ══════════════════════════════════════════════════════════════════════════════
# OXNET stable management APIs
# ══════════════════════════════════════════════════════════════════════════════
@app.get("/api/settings")
async def api_settings(_=Depends(require_auth)):
    ensure_reality_params()
    SETTINGS.setdefault("remark_template", "{status_emoji} {label} · {target}")
    SETTINGS.setdefault("info_templates", [
        "{status_emoji} وضعیت اشتراک: {status}",
        "👤 کاربر: {username}",
        "📦 حجم باقیمانده: {remain_traffic} از {total_traffic}",
        "⏰ زمان باقیمانده: {remain_time}",
    ])
    SETTINGS.setdefault("info_configs_enabled", True)
    return {
        "settings": SETTINGS,
        "host": get_host(),
        "default_host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"]),
        "login_url": get_login_url(),
        "login_path": get_login_path(),
        "dashboard_url": get_dashboard_url(),
        "panel_base": get_panel_base(),
        "app_port": CONFIG["port"],
        "data_dir": str(DATA_DIR),
        "data_persistent": str(DATA_DIR) in ("/data",) or str(DATA_DIR).startswith("/data/") or bool(os.environ.get("DATA_DIR")),
        "remark_vars": [
            "label", "username", "status", "status_emoji", "remain_traffic", "total_traffic",
            "used_traffic", "remain_time", "remain_days", "protocol", "target", "domain",
            "cdn", "cdn_name", "extra_name", "flag", "sub_name",
        ],
        "remark_examples": [
            "{status_emoji} {label} · {cdn_name} · {target}",
            "{flag} {label} - {extra_name} - {target}",
            "{label} | {remain_traffic}/{total_traffic} | {remain_days}d",
        ],
    }


@app.post("/api/settings/reality/generate")
async def api_reality_generate(_=Depends(require_auth)):
    """Regenerate pbk/sid/sni/spx/fp (keeps host & port)."""
    real = SETTINGS.setdefault("reality", {})
    host = real.get("host") or ""
    port = real.get("port") or 443
    gen = generate_reality_params()
    real.update(gen)
    real["host"] = host
    real["port"] = port
    await save_state()
    log_activity("system", "پارامترهای Reality دوباره ساخته شد", "ok")
    # never expose private_key to clients unnecessarily — keep in settings only
    safe = {k: v for k, v in real.items() if k != "private_key"}
    return {"ok": True, "reality": real, "public": safe}

@app.patch("/api/settings")
async def api_update_settings(request: Request, _=Depends(require_auth)):
    body = await request.json()
    # قالب نام کانفیگ و خطوط آماری
    if "remark_template" in body:
        SETTINGS["remark_template"] = str(body.get("remark_template") or "").strip()[:200] or "{status_emoji} {label} · {target}"
    if "info_templates" in body:
        raw = body.get("info_templates")
        if isinstance(raw, str):
            raw = [x.strip() for x in raw.split("\n") if x.strip()]
        if isinstance(raw, list):
            SETTINGS["info_templates"] = [str(x).strip()[:120] for x in raw if str(x).strip()][:20]
    if "info_configs_enabled" in body:
        SETTINGS["info_configs_enabled"] = bool(body.get("info_configs_enabled"))

    for section in ("theme", "security", "cleanup", "panel", "railway_tcp", "reality"):
        if section in body and isinstance(body[section], dict):
            SETTINGS.setdefault(section, {}).update(body[section])
            if section == "panel":
                if "domain" in body["panel"]:
                    SETTINGS["panel"]["domain"] = _norm_domain(str(body["panel"].get("domain") or ""))
                if "login_path" in body["panel"]:
                    SETTINGS["panel"]["login_path"] = normalize_login_path(str(body["panel"].get("login_path") or ""))
            if section == "railway_tcp":
                tcp = SETTINGS.setdefault("railway_tcp", {})
                if "domain" in body["railway_tcp"]:
                    dom = str(body["railway_tcp"].get("domain") or "").strip()
                    dom = re.sub(r"^https?://", "", dom, flags=re.I).split("/", 1)[0].strip()
                    tcp["domain"] = dom
                if "port" in body["railway_tcp"]:
                    try:
                        p = int(body["railway_tcp"].get("port") or 0)
                    except (TypeError, ValueError):
                        p = 0
                    tcp["port"] = p if 0 <= p <= 65535 else 0
                if "path_mode" in body["railway_tcp"]:
                    mode = str(body["railway_tcp"].get("path_mode") or "panel").strip().lower()
                    tcp["path_mode"] = mode if mode in ("panel", "root") else "panel"
            if section == "reality":
                real = SETTINGS.setdefault("reality", {})
                if "host" in body["reality"]:
                    h = str(body["reality"].get("host") or "").strip()
                    h = re.sub(r"^https?://", "", h, flags=re.I).split("/", 1)[0].strip()
                    real["host"] = h
                if "port" in body["reality"]:
                    try:
                        p = int(body["reality"].get("port") or 443)
                    except (TypeError, ValueError):
                        p = 443
                    real["port"] = p if 1 <= p <= 65535 else 443
                for key in ("pbk", "sid", "sni", "fp", "spx"):
                    if key in body["reality"]:
                        real[key] = str(body["reality"].get(key) or "").strip()
                if not real.get("fp"):
                    real["fp"] = "chrome"
                if not real.get("spx"):
                    real["spx"] = "/"
    await save_state()
    log_activity("system", "تنظیمات پیشرفته ذخیره شد", "ok")
    return {
        "ok": True,
        "settings": SETTINGS,
        "host": get_host(),
        "login_url": get_login_url(),
        "login_path": get_login_path(),
        "dashboard_url": get_dashboard_url(),
        "panel_base": get_panel_base(),
    }

@app.get("/api/customers")
async def api_customers(_=Depends(require_auth)):
    async with CUSTOMERS_LOCK:
        return {"customers": [{"customer_id": cid, **c} for cid, c in CUSTOMERS.items()]}

@app.post("/api/customers")
async def api_create_customer(request: Request, _=Depends(require_auth)):
    body = await request.json()
    cid = generate_uuid()
    CUSTOMERS[cid] = {
        "name": str(body.get("name") or "کاربر جدید")[:80],
        "phone": str(body.get("phone") or "")[:40],
        "note": str(body.get("note") or "")[:300],
        "status": str(body.get("status") or "active")[:30],
        "link_ids": list(body.get("link_ids") or []),
        "created_at": datetime.now().isoformat(),
    }
    await save_state()
    return {"ok": True, "customer_id": cid, **CUSTOMERS[cid]}

@app.patch("/api/customers/{cid}")
async def api_update_customer(cid: str, request: Request, _=Depends(require_auth)):
    if cid not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="customer not found")
    body = await request.json()
    for k in ("name", "phone", "note", "status"):
        if k in body: CUSTOMERS[cid][k] = str(body[k])[:300]
    if "link_ids" in body: CUSTOMERS[cid]["link_ids"] = list(body.get("link_ids") or [])
    await save_state()
    return {"ok": True, "customer_id": cid, **CUSTOMERS[cid]}

@app.delete("/api/customers/{cid}")
async def api_delete_customer(cid: str, _=Depends(require_auth)):
    CUSTOMERS.pop(cid, None)
    await save_state()
    return {"ok": True}

@app.get("/api/config-health")
async def api_config_health(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    rows=[]
    now = datetime.now()
    for uid,l in snap.items():
        used=l.get("used_bytes",0); limit=l.get("limit_bytes",0); expired=is_link_expired(l)
        conn_count=sum(1 for c in connections.values() if c.get("uuid")==uid)
        score=100
        reasons=[]
        if not l.get("active", True): score-=45; reasons.append("غیرفعال")
        if expired: score-=45; reasons.append("منقضی")
        if limit and used>=limit: score-=40; reasons.append("سهمیه تمام")
        if conn_count>0: reasons.append("اتصال زنده")
        if "xhttp" in str(l.get("protocol","")) and conn_count==0: score-=5
        status="سالم" if score>=80 else ("نیازمند بررسی" if score>=45 else "خراب/مسدود")
        rows.append({"uuid":uid,"label":l.get("label"),"protocol":l.get("protocol"),"score":max(0,score),"status":status,"reasons":reasons,"used_bytes":used,"limit_bytes":limit,"active_connections":conn_count})
    rows.sort(key=lambda x:x["score"])
    return {"items": rows}

@app.post("/api/smart-subscription")
async def api_smart_subscription(request: Request, _=Depends(require_auth)):
    body = await request.json()
    label = str(body.get("label") or "Smart Iran")[:60]
    profile = str(body.get("profile") or "general")
    protocols = SETTINGS.get("smart_profiles", {}).get(profile) or SETTINGS["smart_profiles"]["general"]
    fake = {"label": label, "protocol": "multi", "custom_path": body.get("custom_path"), "limit_value": body.get("limit_value", 0), "limit_unit": body.get("limit_unit", "GB"), "expires_days": body.get("expires_days", 0), "note": "Smart Subscription"}
    host=get_host(); base_path=await unique_config_path(normalize_config_path(fake.get("custom_path")), generate_uuid()[:8]); sub_id=generate_uuid(); uuid_key=base_path
    limit_bytes=0 if float(fake.get("limit_value") or 0)<=0 else parse_size_to_bytes(float(fake.get("limit_value") or 0), fake.get("limit_unit") or "GB")
    sub={"name":label,"desc":f"Smart Subscription · {profile}","uuid_key":uuid_key,"password_hash":None,"created_at":datetime.now().isoformat(),"link_ids":[],"smart_profile":profile,"limit_bytes":limit_bytes,"used_bytes":0}
    expires_at=(datetime.now()+timedelta(days=int(fake.get("expires_days") or 0))).isoformat() if int(fake.get("expires_days") or 0)>0 else None
    async with LINKS_LOCK:
        for proto in protocols:
            muid=generate_uuid(); mpath=f"{base_path}-{proto_slug(proto)}"; LINKS[muid]={"label":f"{label} - {proto}","limit_bytes":limit_bytes,"used_bytes":0,"created_at":datetime.now().isoformat(),"active":True,"expires_at":expires_at,"note":"Smart Subscription","is_default":False,"sub_id":sub_id,"protocol":proto,"path":mpath,"is_multi_child":True,"multi_group_id":sub_id,"ad_tag":None}; sub["link_ids"].append(muid)
    SUBS[sub_id]=sub
    await save_state()
    return {"ok":True,"sub_id":sub_id,"sub_url":f"https://{host}/sub-group/{uuid_key}","profile":profile,"protocols":protocols}

@app.get("/api/backup/export")
async def api_backup_export(_=Depends(require_auth)):
    return JSONResponse(_state_snapshot(), headers={"Content-Disposition":"attachment; filename=oxnet-backup.json"})

@app.get("/api/backup/restore-points")
async def api_backup_restore_points(_=Depends(require_auth)):
    return {"items": SETTINGS.setdefault("backups", [])[-20:]}

@app.post("/api/backup/save")
async def api_backup_save(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = str(body.get("name") or f"Backup {datetime.now().strftime('%Y-%m-%d %H:%M')}")[:80]
    bid = generate_uuid()
    item = {"id": bid, "name": name, "created_at": datetime.now().isoformat(), "data": _state_snapshot()}
    SETTINGS.setdefault("backups", []).append(item)
    SETTINGS["backups"] = SETTINGS["backups"][-20:]
    await save_state()
    return {"ok": True, "id": bid, "name": name}

@app.post("/api/backup/restore/{bid}")
async def api_backup_restore(bid: str, _=Depends(require_auth)):
    item = next((b for b in SETTINGS.setdefault("backups", []) if b.get("id") == bid), None)
    if not item:
        raise HTTPException(status_code=404, detail="backup not found")
    data = item.get("data") or {}
    LINKS.clear(); LINKS.update(data.get("links", {}))
    SUBS.clear(); SUBS.update(data.get("subs", {}))
    CUSTOMERS.clear(); CUSTOMERS.update(data.get("customers", {}))
    SETTINGS.update(data.get("settings", {}))
    if data.get("password_hash"):
        AUTH["password_hash"] = data["password_hash"]
    await save_state()
    log_activity("system", f"ریستور بکاپ «{item.get('name','')}» انجام شد", "ok")
    return {"ok": True, "restored": item.get("name")}

@app.post("/api/backup/import")
async def api_backup_import(request: Request, _=Depends(require_auth)):
    data = await request.json()
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="backup invalid")
    LINKS.clear(); LINKS.update(data.get("links", {}))
    SUBS.clear(); SUBS.update(data.get("subs", {}))
    CUSTOMERS.clear(); CUSTOMERS.update(data.get("customers", {}))
    SETTINGS.update(data.get("settings", {}))
    if data.get("password_hash"): AUTH["password_hash"] = data["password_hash"]
    await save_state(); log_activity("system", "بکاپ ایمپورت شد", "ok")
    return {"ok": True, "links": len(LINKS), "subs": len(SUBS), "customers": len(CUSTOMERS)}

@app.get("/api/monitoring")
async def api_monitoring(_=Depends(require_auth)):
    async with LINKS_LOCK: snap=dict(LINKS)
    proto={}
    for l in snap.values(): proto[l.get("protocol",DEFAULT_PROTOCOL)] = proto.get(l.get("protocol",DEFAULT_PROTOCOL),0)+1
    ipmap={}
    for c in connections.values(): ipmap[c.get("ip","?")] = ipmap.get(c.get("ip","?"),0)+1
    return {"protocols":proto,"top_ips":sorted(ipmap.items(), key=lambda x:x[1], reverse=True)[:10],"top_links":sorted([{"label":l.get("label"),"used_bytes":l.get("used_bytes",0),"protocol":l.get("protocol")} for l in snap.values()], key=lambda x:x["used_bytes"], reverse=True)[:10],"errors":list(error_logs)[-20:],"db_mode":"JSON File"}

@app.post("/api/cleanup/run")
async def api_cleanup_run(request: Request, _=Depends(require_auth)):
    body=await request.json(); expired_days=int(body.get("expired_days",0) or 0); reset_logs=bool(body.get("reset_logs",False)); inactive_days=int(body.get("inactive_days",0) or 0)
    deleted=[]; archived=[]; now=datetime.now()
    async with LINKS_LOCK:
        for uid,l in list(LINKS.items()):
            if expired_days and l.get("expires_at"):
                try:
                    if (now-datetime.fromisoformat(l["expires_at"])).days>=expired_days:
                        deleted.append(uid); del LINKS[uid]; continue
                except Exception: pass
            if inactive_days and not l.get("active",True):
                l["archived"] = True; archived.append(uid)
    if reset_logs:
        error_logs.clear(); activity_logs.clear()
    await save_state()
    return {"ok":True,"deleted":len(deleted),"archived":len(archived),"logs_reset":reset_logs}

# ══════════════════════════════════════════════════════════════════════════════
# Version / Auto-Update
# ══════════════════════════════════════════════════════════════════════════════
update_log = deque(maxlen=100)
update_state = {"running": False, "progress": 0}
def load_update_history(): return []

@app.get("/api/version")
async def api_version(_=Depends(require_auth)):
    current_info = {"version": get_current_panel_version(), "description": "نسخه نصب‌شده OXNET"}
    return {"repo": "standalone", "branch": "local", "current": current_info, "latest": current_info, "update_available": False}

@app.get("/api/update-history")
async def api_update_history(_=Depends(require_auth)):
    return {"history": load_update_history()}

@app.get("/api/update-log")
async def api_update_log(_=Depends(require_auth)):
    return {"running": update_state["running"], "progress": update_state["progress"], "logs": list(update_log)[-100:]}

@app.post("/api/update")
async def api_update(_=Depends(require_auth)):
    raise HTTPException(status_code=404, detail="بروزرسانی خودکار در نسخه مستقل OXNET حذف شده است")


# ── HTML Pages ───────────────────────────────────────────────────────────────
from pages import LOGIN_HTML, DASHBOARD_HTML

def render_html(html: str) -> str:
    v = get_current_panel_version()
    return html.replace("v1.0.0", f"v{v}").replace("v1.1.0", f"v{v}").replace("v1.2.0", f"v{v}").replace("v1.2.1", f"v{v}").replace("v2.0.0", f"v{v}").replace("v2.0.1", f"v{v}").replace("v2.0.2", f"v{v}").replace("v2.0.3", f"v{v}").replace("v2.0.4", f"v{v}").replace("v2.0.5", f"v{v}").replace("v2.0.6", f"v{v}").replace("v2.0.7", f"v{v}").replace("v2.0.8", f"v{v}").replace("v2.0.9", f"v{v}").replace("v2.0.10", f"v{v}").replace("v2.0.11", f"v{v}").replace("v2.0.12", f"v{v}").replace("v2.0.13", f"v{v}").replace("v2.0.14", f"v{v}").replace("v2.0.15", f"v{v}").replace("v2.0.16", f"v{v}").replace("v2.0.17", f"v{v}").replace("v3.0.0", f"v{v}").replace("· 1.0.0", f"· {v}").replace("· 1.1.0", f"· {v}").replace("· 1.2.0", f"· {v}").replace("· 1.2.1", f"· {v}").replace("· 2.0.0", f"· {v}").replace("· 2.0.1", f"· {v}").replace("· 2.0.2", f"· {v}").replace("· 2.0.3", f"· {v}").replace("· 2.0.4", f"· {v}").replace("· 2.0.5", f"· {v}").replace("· 2.0.6", f"· {v}").replace("· 2.0.7", f"· {v}").replace("· 2.0.8", f"· {v}").replace("· 2.0.9", f"· {v}").replace("· 2.0.10", f"· {v}").replace("· 2.0.11", f"· {v}")


# ── Central: Announcements & Support ─────────────────────────────────────────
@app.get("/api/announcements")
async def api_announcements(_=Depends(require_auth)):
    return {"announcements": []}

@app.post("/api/announcements/view")
async def api_announcements_view(request: Request, _=Depends(require_auth)):
    return {"ok": True}

@app.get("/api/support/messages")
async def api_support_messages(_=Depends(require_auth)):
    return {"messages": [], "blocked": False}

@app.post("/api/support/send")
async def api_support_send(request: Request, _=Depends(require_auth)):
    raise HTTPException(status_code=404, detail="این بخش در نسخه مستقل OXNET حذف شده است")


def _not_found_html() -> HTMLResponse:
    html = (
        "<!DOCTYPE html><html lang='fa' dir='rtl'><head><meta charset='UTF-8'><title>404</title>"
        "<style>body{font-family:system-ui,sans-serif;background:#F8FAFC;color:#0F172A;"
        "display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0}"
        ".b{text-align:center}.c{font-size:56px;font-weight:700;color:#94A3B8}"
        "p{color:#64748B;margin-top:8px}</style></head><body><div class='b'><div class='c'>404</div>"
        "<p>صفحه پیدا نشد</p></div></body></html>"
    )
    return HTMLResponse(content=html, status_code=404)


def _inject_panel_base(html: str) -> str:
    base = get_panel_base()
    boot = "<script>window.OXNET_BASE=" + repr(base) + ";window.OXNET_LOGIN=" + repr(get_login_url()) + ";window.OXNET_DASH=" + repr(get_dashboard_url()) + ";</script>"
    if "<head>" in html:
        return html.replace("<head>", "<head>" + boot, 1)
    return boot + html


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # اگر مسیر مخفی تنظیم شده، /login خام را مخفی کن (HTML 404 نه JSON)
    secret = get_login_path()
    if secret:
        return _not_found_html()
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(get_dashboard_url(), status_code=302)
    return HTMLResponse(content=_inject_panel_base(render_html(LOGIN_HTML)))


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if get_login_path():
        return _not_found_html()
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(get_login_url(), status_code=302)
    await ensure_default_link()
    return HTMLResponse(content=_inject_panel_base(render_html(DASHBOARD_HTML)))


@app.get("/{login_slug}/login", response_class=HTMLResponse)
async def custom_login_page(login_slug: str, request: Request):
    expected = get_login_path()
    if not expected or normalize_login_path(login_slug) != expected:
        return _not_found_html()
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(get_dashboard_url(), status_code=302)
    return HTMLResponse(content=_inject_panel_base(render_html(LOGIN_HTML)))


@app.get("/{login_slug}/dashboard", response_class=HTMLResponse)
async def custom_dashboard(login_slug: str, request: Request):
    expected = get_login_path()
    if not expected or normalize_login_path(login_slug) != expected:
        return _not_found_html()
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(get_login_url(), status_code=302)
    await ensure_default_link()
    return HTMLResponse(content=_inject_panel_base(render_html(DASHBOARD_HTML)))


@app.get("/test-ws", response_class=HTMLResponse)
async def test_ws_redirect():
    return RedirectResponse(get_dashboard_url(), status_code=302)


# ── WebSocket / tunnel routes ─────────────────────────────────────────────────
# NOTE: Do NOT register @app.websocket("/") — it can break Railway HTTP health on "/".
# Root path=/ is handled by VlessRootMiddleware below (websocket only).

@app.websocket("/ws/{uuid}")
async def ws_vless_path(ws: WebSocket, uuid: str):
    from relay_vless import websocket_tunnel
    await websocket_tunnel(ws, uuid)


@app.websocket("/vless-tcp")
async def ws_vless_tcp_alias(ws: WebSocket):
    """Alias for TCP-proxy clients that use path=/vless-tcp."""
    from relay_vless import websocket_tunnel_root
    await websocket_tunnel_root(ws)


@app.websocket("/trojan-ws")
async def ws_trojan(ws: WebSocket):
    from trojan import trojan_ws_tunnel
    await trojan_ws_tunnel(ws)


@app.websocket("/ss/{uuid}")
async def ws_shadowsocks(ws: WebSocket, uuid: str):
    from shadowsocks_ws import shadowsocks_ws_tunnel
    await shadowsocks_ws_tunnel(ws, uuid)


# مسیر ساده /{token} — فقط path رندوم در لینک‌ها
_RESERVED_WS_PATHS = {
    "r",
    "api", "login", "dashboard", "health", "stats", "sub", "sub-all", "sub-group",
    "ws", "ss", "trojan-ws", "vless-tcp", "xhttp-siz10", "static", "assets", "docs",
    "openapi.json", "p", "proxy", "cf-sub", "domain-sub", "test-ws", "support",
    "cluster", "settings", "customers", "cloudflare", "connections", "traffic",
}

@app.websocket("/{token}")
async def ws_by_custom_path(ws: WebSocket, token: str):
    """WebSocket روی path ساده مثل /kdkdjsjdj بر اساس path ذخیره‌شده کانفیگ."""
    tok = (token or "").strip().strip("/")
    if not tok or tok in _RESERVED_WS_PATHS or "/" in tok:
        await ws.close(code=1008)
        return
    uid = await resolve_link_id(tok)
    if not uid:
        # شاید خود uuid باشد
        uid = tok if tok in LINKS else None
    if not uid:
        await ws.close(code=1008, reason="unknown path")
        return
    link = LINKS.get(uid) or {}
    proto = str(link.get("protocol") or "vless-ws")
    if proto == "trojan-ws":
        from trojan import trojan_ws_tunnel
        # trojan tunnel ممکن است path ثابت بخواهد؛ uuid را پاس بده
        try:
            await trojan_ws_tunnel(ws, uid)
        except TypeError:
            await trojan_ws_tunnel(ws)
        return
    if proto == "shadowsocks-tls":
        from shadowsocks_ws import shadowsocks_ws_tunnel
        await shadowsocks_ws_tunnel(ws, uid)
        return
    from relay_vless import websocket_tunnel
    await websocket_tunnel(ws, uid)


# ══════════════════════════════════════════════════════════════════════════════
# Cluster: Central panel ↔ Node panels (multi-region Railway)
# ══════════════════════════════════════════════════════════════════════════════

def _cluster() -> dict:
    c = SETTINGS.setdefault("cluster", {
        "role": "standalone", "node_name": "", "region": "",
        "central_url": "", "node_token": "", "cluster_secret": "", "auto_sync": True,
    })
    return c


def _cluster_role() -> str:
    role = str(_cluster().get("role") or "standalone").strip().lower()
    return role if role in ("standalone", "central", "node") else "standalone"


def _verify_node_token(request: Request) -> dict | None:
    """Validate node token from Authorization Bearer or X-Node-Token."""
    token = ""
    auth = request.headers.get("authorization") or ""
    if auth.lower().startswith("bearer "):
        token = auth[7:].strip()
    if not token:
        token = (request.headers.get("x-node-token") or "").strip()
    if not token:
        return None
    for nid, node in NODES.items():
        if str(node.get("token") or "") == token:
            return {"id": nid, **node}
    return None



def _node_base_url(node: dict) -> str:
    host = str(node.get("host") or "").strip().rstrip("/")
    if not host:
        return ""
    return host if host.startswith("http") else "https://" + host


async def _send_node_control(node_id: str, source_ids: list[str], action: str, value=None) -> bool:
    """مرکزی → نود: اعمال وضعیت یا UUID روی کل کانفیگ/گروه بدون نیاز به ورود ادمین نود."""
    async with NODES_LOCK:
        node = dict(NODES.get(node_id) or {})
    base = _node_base_url(node)
    token = str(node.get("token") or "")
    if not base or not token:
        return False
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            r = await client.post(
                f"{base}/api/cluster/control",
                headers={"X-Node-Token": token, "Authorization": f"Bearer {token}"},
                json={"action": action, "source_ids": source_ids, "value": value},
            )
        return r.status_code < 400
    except Exception as exc:
        logger.warning("node control failed %s: %s", node_id, exc)
        return False


async def _control_remote_links(link_ids: list[str], action: str, value=None) -> dict:
    grouped: dict[str, list[str]] = {}
    for rid in link_ids:
        parts = str(rid).split(":", 2)
        if len(parts) == 3 and parts[0] == "remote":
            grouped.setdefault(parts[1], []).append(parts[2])
    results = await asyncio.gather(*[
        _send_node_control(nid, list(dict.fromkeys(source_ids)), action, value)
        for nid, source_ids in grouped.items()
    ]) if grouped else []
    return {"nodes": len(grouped), "delivered": sum(1 for x in results if x)}


@app.post("/api/cluster/control")
async def api_cluster_control(request: Request):
    """روی نود: فرمان امضاشده مرکزی را روی کانفیگ‌های واقعی اعمال می‌کند."""
    if _cluster_role() != "node":
        raise HTTPException(status_code=403, detail="این پنل نود نیست")
    c = _cluster()
    auth = request.headers.get("authorization") or ""
    token = auth[7:].strip() if auth.lower().startswith("bearer ") else (request.headers.get("x-node-token") or "").strip()
    if not token or token != str(c.get("node_token") or ""):
        raise HTTPException(status_code=401, detail="توکن مرکزی نامعتبر است")
    body = await request.json()
    action = str(body.get("action") or "")
    source_ids = [str(x) for x in (body.get("source_ids") or [])]
    base_ids = {x.split(":", 1)[0] for x in source_ids if x}
    apply_all = action in ("disable_all", "enable_all") and not base_ids
    changed = 0
    async with LINKS_LOCK:
        for uid, link in LINKS.items():
            if not apply_all and uid not in base_ids:
                continue
            if action == "disable_all":
                link["active"] = False
                changed += 1
            elif action == "enable_all":
                link["active"] = True
                changed += 1
            elif action == "set_active":
                link["active"] = _as_bool(body.get("value"))
                changed += 1
            elif action == "set_uuid_alias":
                alias = str(body.get("value") or "").strip()
                if alias:
                    link["cluster_uuid_alias"] = alias
                    aliases = link.setdefault("uuid_aliases", [])
                    if alias not in aliases:
                        aliases.append(alias)
                    changed += 1
    if changed:
        await save_state()
    return {"ok": True, "changed": changed}


@app.get("/api/cluster/status")
async def api_cluster_status(_=Depends(require_auth)):
    c = _cluster()
    role = _cluster_role()
    async with NODES_LOCK:
        nodes_snap = [
            {
                "id": nid,
                "name": n.get("name"),
                "region": n.get("region"),
                "host": n.get("host"),
                "last_seen": n.get("last_seen"),
                "config_count": len(n.get("configs") or []),
                "online": bool(n.get("last_seen")),
                "last_ping_ms": n.get("last_ping_ms"),
                "last_ping_ok": n.get("last_ping_ok"),
                "last_ping_at": n.get("last_ping_at"),
            }
            for nid, n in NODES.items()
        ]
    return {
        "role": role,
        "cluster": {
            "role": role,
            "node_name": c.get("node_name") or "",
            "region": c.get("region") or "",
            "central_url": c.get("central_url") or "",
            "has_node_token": bool(c.get("node_token")),
            "has_cluster_secret": bool(c.get("cluster_secret")),
            "auto_sync": bool(c.get("auto_sync")),
            "sync_main": _as_bool(c.get("sync_main", True)),
            "sync_extra": _as_bool(c.get("sync_extra", True)),
            "sync_cf": _as_bool(c.get("sync_cf", False)),
            # secret فقط روی مرکزی و فقط به ادمین لاگین‌شده
            "cluster_secret": c.get("cluster_secret") or "" if role == "central" else "",
            "node_token": c.get("node_token") or "" if role == "node" else "",
        },
        "nodes": nodes_snap if role == "central" else [],
        "local_host": get_host(),
        "remote_config_count": sum(len(n.get("configs") or []) for n in NODES.values()) if role == "central" else 0,
        "selected_local_count": sum(1 for l in LINKS.values() if _as_bool(l.get("sync_to_central", True))) if role == "node" else 0,
    }


@app.patch("/api/cluster/settings")
async def api_cluster_settings(request: Request, _=Depends(require_auth)):
    body = await request.json()
    c = _cluster()
    if "role" in body:
        role = str(body.get("role") or "standalone").strip().lower()
        c["role"] = role if role in ("standalone", "central", "node") else "standalone"
    if "node_name" in body:
        c["node_name"] = str(body.get("node_name") or "").strip()[:60]
    if "region" in body:
        c["region"] = str(body.get("region") or "").strip()[:40]
    if "central_url_secondary" in body:
        c["central_url_secondary"] = str(body.get("central_url_secondary") or "").strip()
    if "central_url" in body:
        url = str(body.get("central_url") or "").strip().rstrip("/")
        if url and not url.startswith("http"):
            url = "https://" + url
        c["central_url"] = url[:200]
    if "auto_sync" in body:
        c["auto_sync"] = bool(body.get("auto_sync"))
    if "node_token" in body:
        c["node_token"] = str(body.get("node_token") or "").strip()[:120]
    if "sync_main" in body:
        c["sync_main"] = _as_bool(body.get("sync_main"))
    if "sync_extra" in body:
        c["sync_extra"] = _as_bool(body.get("sync_extra"))
    if "sync_cf" in body:
        c["sync_cf"] = _as_bool(body.get("sync_cf"))
    await save_state()
    log_activity("system", f"تنظیمات کلاستر ذخیره شد (role={c.get('role')})", "ok")
    return {"ok": True, "role": c.get("role")}


@app.post("/api/cluster/generate-secret")
async def api_cluster_generate_secret(_=Depends(require_auth)):
    if _cluster_role() != "central":
        raise HTTPException(status_code=400, detail="فقط پنل مرکزی می‌تواند Secret بسازد")
    c = _cluster()
    c["cluster_secret"] = secrets.token_urlsafe(24)
    await save_state()
    log_activity("system", "Cluster Secret جدید ساخته شد", "ok")
    return {"ok": True, "cluster_secret": c["cluster_secret"]}


@app.post("/api/cluster/register")
async def api_cluster_register(request: Request):
    """نود → مرکزی: ثبت‌نام با cluster_secret."""
    if _cluster_role() != "central":
        raise HTTPException(status_code=403, detail="این پنل مرکزی نیست")
    body = await request.json()
    secret = str(body.get("cluster_secret") or body.get("secret") or "").strip()
    c = _cluster()
    if not c.get("cluster_secret") or secret != c.get("cluster_secret"):
        raise HTTPException(status_code=403, detail="Cluster Secret نامعتبر است")
    name = str(body.get("name") or body.get("node_name") or "Node").strip()[:60] or "Node"
    region = str(body.get("region") or "").strip()[:40]
    host = str(body.get("host") or "").strip()[:120]
    host = re.sub(r"^https?://", "", host, flags=re.I).split("/", 1)[0].strip()
    node_id = str(body.get("node_id") or "").strip() or generate_uuid()
    token = secrets.token_urlsafe(32)
    async with NODES_LOCK:
        # اگر همین host قبلاً ثبت شده، به‌روزرسانی
        for nid, n in list(NODES.items()):
            if host and n.get("host") == host:
                node_id = nid
                token = n.get("token") or token
                break
        NODES[node_id] = {
            "name": name,
            "region": region,
            "host": host,
            "token": token,
            "last_seen": datetime.now().isoformat(),
            "configs": NODES.get(node_id, {}).get("configs") or [],
            "created_at": NODES.get(node_id, {}).get("created_at") or datetime.now().isoformat(),
        }
    await save_state()
    log_activity("system", f"نود «{name}» ثبت شد ({region or host})", "ok")
    return {
        "ok": True,
        "node_id": node_id,
        "node_token": token,
        "central_host": get_host(),
    }


@app.post("/api/cluster/push")
async def api_cluster_push(request: Request):
    """نود → مرکزی: ارسال لیست کانفیگ‌ها (share URI)."""
    if _cluster_role() != "central":
        raise HTTPException(status_code=403, detail="این پنل مرکزی نیست")
    node = _verify_node_token(request)
    if not node:
        raise HTTPException(status_code=401, detail="node token نامعتبر است")
    body = await request.json()
    configs = body.get("configs") or []
    if not isinstance(configs, list):
        raise HTTPException(status_code=400, detail="configs must be a list")
    clean = []
    for item in configs[:500]:
        if isinstance(item, str):
            uri = item.strip()
            if uri:
                clean.append({"label": "config", "uri": uri, "protocol": ""})
        elif isinstance(item, dict):
            uri = str(item.get("uri") or item.get("link") or "").strip()
            if not uri:
                continue
            clean.append({
                "label": str(item.get("label") or item.get("name") or "config")[:100],
                "uri": uri[:2000],
                "protocol": str(item.get("protocol") or "")[:40],
                "active": bool(item.get("active", True)),
                "source_id": str(item.get("source_id") or "")[:160],
                "domain_kind": str(item.get("domain_kind") or "")[:40],
                "target": str(item.get("target") or "")[:120],
                "group_ids": [str(x)[:160] for x in (item.get("group_ids") or [])[:20]],
                "group_names": [str(x)[:100] for x in (item.get("group_names") or [])[:20]],
                "canonical_uuid": str(item.get("canonical_uuid") or "")[:64],
                "used_bytes": max(0, int(item.get("used_bytes") or 0)),
            })
    nid = node["id"]
    async with NODES_LOCK:
        if nid not in NODES:
            raise HTTPException(status_code=404, detail="node not found")
        NODES[nid]["configs"] = clean
        NODES[nid]["last_seen"] = datetime.now().isoformat()
        if body.get("name"):
            NODES[nid]["name"] = str(body.get("name"))[:60]
        if body.get("region"):
            NODES[nid]["region"] = str(body.get("region"))[:40]
        if body.get("host"):
            h = re.sub(r"^https?://", "", str(body.get("host")), flags=re.I).split("/", 1)[0].strip()
            NODES[nid]["host"] = h[:120]
    await save_state()
    return {"ok": True, "accepted": len(clean)}


@app.post("/api/cluster/usage")
async def api_cluster_usage(request: Request):
    """نود → مرکزی: گزارش مصرف تا از سهمیه اشتراک مرکزی کم شود."""
    if _cluster_role() != "central":
        raise HTTPException(status_code=403, detail="این پنل مرکزی نیست")
    node = _verify_node_token(request)
    if not node:
        raise HTTPException(status_code=401, detail="node token نامعتبر است")
    body = await request.json()
    try:
        n = int(body.get("bytes") or body.get("n") or 0)
    except Exception:
        n = 0
    if n <= 0:
        return {"ok": True, "allowed": True, "charged": 0}
    uuid_key = str(body.get("uuid") or body.get("source_id") or "").strip()
    if not uuid_key:
        return {"ok": True, "allowed": True, "charged": 0}

    nid = node["id"]
    matched_rids: list[str] = []
    async with NODES_LOCK:
        node_rec = NODES.get(nid) or {}
        for idx, cfg in enumerate(node_rec.get("configs") or []):
            if not isinstance(cfg, dict):
                continue
            sid = str(cfg.get("source_id") if cfg.get("source_id") not in (None, "") else idx)
            # source_id مثل uuid:main یا uuid:extra:...
            if sid == uuid_key or sid.startswith(uuid_key + ":") or uuid_key.startswith(sid.split(":")[0]):
                cfg["used_bytes"] = int(cfg.get("used_bytes") or 0) + n
                matched_rids.append(f"remote:{nid}:{sid}")
        # اگر هیچ match نبود، با خود uuid به‌عنوان source
        if not matched_rids:
            matched_rids.append(f"remote:{nid}:{uuid_key}")

    charged_subs: list[str] = []
    async with SUBS_LOCK:
        async with LINKS_LOCK:
            for sid, s in SUBS.items():
                lids = [str(x) for x in (s.get("link_ids") or [])]
                if not any(r in lids for r in matched_rids):
                    continue
                _charge_sub_usage(sid, n)
                charged_subs.append(sid)

    allowed = True
    for sid in charged_subs:
        if _sub_quota_exceeded(SUBS.get(sid)):
            allowed = False
            break
    # اگر هیچ ساب‌ی match نشد، همچنان ok (ممکن است هنوز به ساب وصل نباشد)
    if not charged_subs:
        allowed = True

    # ذخیرهٔ دوره‌ای سبک — هر بار ننویس؛ فقط وقتی شارژ شده
    if charged_subs:
        await save_state()
    bump_hourly(n)
    stats["total_bytes"] = int(stats.get("total_bytes") or 0) + n
    return {
        "ok": True,
        "allowed": allowed,
        "charged": n,
        "subs": charged_subs,
        "matched": matched_rids[:20],
    }


@app.get("/api/cluster/nodes")
async def api_cluster_nodes(_=Depends(require_auth)):
    if _cluster_role() != "central":
        return {"nodes": [], "role": _cluster_role()}
    async with NODES_LOCK:
        out = []
        for nid, n in NODES.items():
            out.append({
                "id": nid,
                "name": n.get("name"),
                "region": n.get("region"),
                "host": n.get("host"),
                "last_seen": n.get("last_seen"),
                "config_count": len(n.get("configs") or []),
                "configs": n.get("configs") or [],
                "last_ping_ms": n.get("last_ping_ms"),
                "last_ping_at": n.get("last_ping_at"),
                "last_ping_ok": n.get("last_ping_ok"),
            })
    return {"nodes": out, "role": "central"}


async def _measure_node_ping(host: str) -> dict:
    """پینگ واقعی: زمان پاسخ HTTP به /health یا اتصال TLS روی 443."""
    raw = re.sub(r"^https?://", "", str(host or "").strip(), flags=re.I).split("/", 1)[0].strip()
    if not raw or raw in ("localhost", "127.0.0.1"):
        return {"ok": False, "ms": None, "detail": "local"}
    hostname = raw.split(":")[0]
    port = 443
    if ":" in raw:
        try:
            port = int(raw.split(":")[1])
        except Exception:
            port = 443
    t0 = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=3.0, follow_redirects=True, verify=False) as client:
            url = f"https://{hostname}:{port}/health" if port != 443 else f"https://{hostname}/health"
            r = await client.get(url)
            ms = int((time.perf_counter() - t0) * 1000)
            return {"ok": r.status_code < 500, "ms": ms, "status_code": r.status_code}
    except Exception:
        pass
    # fallback: TCP connect
    t0 = time.perf_counter()
    try:
        conn = asyncio.open_connection(hostname, port)
        reader, writer = await asyncio.wait_for(conn, timeout=2.5)
        ms = int((time.perf_counter() - t0) * 1000)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return {"ok": True, "ms": ms, "status_code": 0, "via": "tcp"}
    except Exception as exc:
        ms = int((time.perf_counter() - t0) * 1000)
        return {"ok": False, "ms": ms if ms < 3500 else None, "detail": str(exc)[:80]}


@app.post("/api/cluster/nodes/ping")
async def api_cluster_nodes_ping(request: Request, _=Depends(require_auth)):
    """پینگ واقعی همه نودها یا لیست id."""
    if _cluster_role() != "central":
        raise HTTPException(status_code=400, detail="فقط پنل مرکزی")
    try:
        body = await request.json()
    except Exception:
        body = {}
    want = body.get("ids") if isinstance(body, dict) else None
    async with NODES_LOCK:
        items = []
        for nid, n in NODES.items():
            if want and nid not in want:
                continue
            items.append((nid, n.get("host") or ""))
    results = {}
    async def one(nid, host):
        res = await _measure_node_ping(host)
        results[nid] = res
        async with NODES_LOCK:
            if nid in NODES:
                NODES[nid]["last_ping_ms"] = res.get("ms")
                NODES[nid]["last_ping_ok"] = bool(res.get("ok"))
                NODES[nid]["last_ping_at"] = datetime.now().isoformat()
    await asyncio.gather(*[one(nid, host) for nid, host in items])
    ok_n = sum(1 for v in results.values() if v.get("ok"))
    avg = None
    vals = [v["ms"] for v in results.values() if isinstance(v.get("ms"), int)]
    if vals:
        avg = int(sum(vals) / len(vals))
    return {"ok": True, "results": results, "online": ok_n, "total": len(results), "avg_ms": avg}


@app.delete("/api/cluster/nodes/{node_id}")
async def api_cluster_node_delete(node_id: str, _=Depends(require_auth)):
    async with NODES_LOCK:
        if node_id not in NODES:
            raise HTTPException(status_code=404, detail="node not found")
        name = NODES[node_id].get("name")
        del NODES[node_id]
    await save_state()
    log_activity("system", f"نود «{name}» حذف شد", "warn")
    return {"ok": True}


@app.post("/api/cluster/connect")
async def api_cluster_connect(request: Request, _=Depends(require_auth)):
    """از پنل نود: ثبت‌نام روی مرکزی با secret."""
    if _cluster_role() != "node":
        raise HTTPException(status_code=400, detail="نقش پنل باید Node باشد")
    body = await request.json()
    c = _cluster()
    central = (body.get("central_url") or c.get("central_url") or "").strip().rstrip("/")
    secret = (body.get("cluster_secret") or body.get("secret") or "").strip()
    if not central or not secret:
        raise HTTPException(status_code=400, detail="central_url و cluster_secret لازم است")
    if not central.startswith("http"):
        central = "https://" + central
    payload = {
        "cluster_secret": secret,
        "name": body.get("node_name") or c.get("node_name") or get_host(),
        "region": body.get("region") or c.get("region") or "",
        "host": get_host(),
    }
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            r = await client.post(f"{central}/api/cluster/register", json=payload)
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                raise HTTPException(status_code=400, detail=data.get("detail") or f"central error {r.status_code}")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"اتصال به مرکزی ناموفق: {exc}")
    c["central_url"] = central
    c["node_token"] = str(data.get("node_token") or "")
    c["node_name"] = payload["name"]
    c["region"] = payload["region"]
    c["role"] = "node"
    c["auto_sync"] = True
    await save_state()
    log_activity("system", f"به پنل مرکزی وصل شد: {central}", "ok")
    return {"ok": True, "node_token": c["node_token"], "central_url": central}


def _node_sync_share_variants(uid: str, link: dict, host: str, c: dict) -> list[dict]:
    """بر اساس تنظیمات نود: دامنه اصلی / فرعی(+تمیز) / کلادفلیر را برای ارسال به مرکزی بساز."""
    proto = link.get("protocol") or DEFAULT_PROTOCOL
    label = link.get("label") or uid[:8]
    want_main = _as_bool(c.get("sync_main", True))
    want_extra = _as_bool(c.get("sync_extra", True))
    want_cf = _as_bool(c.get("sync_cf", False))
    # اگر هیچ‌کدام روشن نباشد، حداقل دامنه اصلی
    if not (want_main or want_extra or want_cf):
        want_main = True

    out: list[dict] = []

    def _add(uri: str, source_id: str, tag: str, target: str):
        if not uri:
            return
        group_ids = []
        group_names = []
        for local_sid, local_sub in SUBS.items():
            if uid in (local_sub.get("link_ids") or []) or local_sid in (link.get("sub_id"), link.get("multi_group_id")):
                group_ids.append(str(local_sid))
                group_names.append(str(local_sub.get("name") or "گروه بدون نام"))
        out.append({
            "label": f"{label} · {tag}" if tag and tag != "main" else label,
            "uri": uri,
            "protocol": proto,
            "active": _as_bool(link.get("active", True)),
            "source_id": source_id,
            "domain_kind": tag,
            "target": target,
            "group_ids": group_ids,
            "group_names": group_names,
            "canonical_uuid": str(link.get("cluster_uuid_alias") or ""),
        })

    if want_main:
        try:
            remark = format_config_remark(link, target=host, domain=host, cdn=False)
            uri = generate_share_link(uid, host, remark=remark, protocol=proto, credential_uuid=link.get("cluster_uuid_alias"))
            _add(uri, f"{uid}:main", "main", host)
        except Exception:
            pass

    if want_extra:
        for ed in _extra_domains():
            domain = ed.get("domain") or ""
            if not domain:
                continue
            clean_ips = ed.get("clean_ips") or []
            targets = clean_ips if clean_ips else [domain]
            extra_name = str(ed.get("name") or domain)
            slug = ed.get("slug") or _cf_slug(domain)
            for target in targets:
                try:
                    remark = format_config_remark(
                        link, target=str(target), domain=domain, cdn=False,
                        cdn_name=extra_name, extra_name=extra_name,
                    )
                    uri = generate_share_link(uid, str(target), remark=remark, protocol=proto, sni_host=domain, credential_uuid=link.get("cluster_uuid_alias"))
                    sid = f"{uid}:extra:{slug}:{target}"
                    _add(uri, sid, extra_name, str(target))
                except Exception:
                    continue

    if want_cf:
        for cf in _cf_domains():
            domain = cf.get("domain") or ""
            if not domain:
                continue
            clean_ips = cf.get("clean_ips") or []
            targets = clean_ips if clean_ips else [domain]
            cdn_name = str(cf.get("name") or domain)
            slug = cf.get("slug") or _cf_slug(domain)
            for target in targets:
                try:
                    remark = format_config_remark(
                        link, target=str(target), domain=domain, cdn=True,
                        cdn_name=cdn_name, extra_name=cdn_name,
                    )
                    uri = generate_share_link(uid, str(target), remark=remark, protocol=proto, sni_host=domain, credential_uuid=link.get("cluster_uuid_alias"))
                    sid = f"{uid}:cf:{slug}:{target}"
                    _add(uri, sid, cdn_name, str(target))
                except Exception:
                    continue

    return out



class _JsonRequest:
    def __init__(self, data=None):
        self._data = data or {}
    async def json(self):
        return self._data


async def _cluster_auto_sync_loop():
    """نود متصل، تغییرات را حداکثر طی چند ثانیه به مرکزی می‌فرستد."""
    await asyncio.sleep(3)
    while True:
        try:
            c = _cluster()
            if _cluster_role() == "node" and c.get("node_token") and c.get("central_url") and _as_bool(c.get("auto_sync", True)):
                await api_cluster_sync_now(_JsonRequest(), True)
        except Exception as exc:
            logger.debug("automatic cluster sync failed: %s", exc)
        await asyncio.sleep(6)


@app.post("/api/cluster/sync-now")
async def api_cluster_sync_now(request: Request, _=Depends(require_auth)):
    """از پنل نود: ارسال کانفیگ‌های انتخاب‌شده با دامنه اصلی / فرعی / هر دو به مرکزی."""
    if _cluster_role() != "node":
        raise HTTPException(status_code=400, detail="فقط نود می‌تواند همگام‌سازی کند")
    c = _cluster()
    # امکان override لحظه‌ای از body
    try:
        body = await request.json()
    except Exception:
        body = {}
    if isinstance(body, dict):
        if "sync_main" in body:
            c["sync_main"] = _as_bool(body.get("sync_main"))
        if "sync_extra" in body:
            c["sync_extra"] = _as_bool(body.get("sync_extra"))
        if "sync_cf" in body:
            c["sync_cf"] = _as_bool(body.get("sync_cf"))

    central = (c.get("central_url") or "").strip().rstrip("/")
    token = (c.get("node_token") or "").strip()
    if not central or not token:
        raise HTTPException(status_code=400, detail="ابتدا به مرکزی وصل شوید")
    host = get_host()
    configs = []
    async with LINKS_LOCK:
        for uid, link in LINKS.items():
            if not is_link_allowed(link):
                continue
            if not _as_bool(link.get("sync_to_central", True)):
                continue
            proto = link.get("protocol") or DEFAULT_PROTOCOL
            if proto == "multi":
                continue
            configs.extend(_node_sync_share_variants(uid, link, host, c))
    payload = {
        "name": c.get("node_name") or host,
        "region": c.get("region") or "",
        "host": host,
        "configs": configs,
    }
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            r = await client.post(
                f"{central}/api/cluster/push",
                json=payload,
                headers={"Authorization": f"Bearer {token}", "X-Node-Token": token},
            )
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                raise HTTPException(status_code=400, detail=data.get("detail") or f"push failed {r.status_code}")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"ارسال به مرکزی ناموفق: {exc}")
    await save_state()
    log_activity(
        "system",
        f"همگام‌سازی نود: {len(configs)} لینک (main={c.get('sync_main')} extra={c.get('sync_extra')} cf={c.get('sync_cf')})",
        "ok",
    )
    return {
        "ok": True,
        "sent": len(configs),
        "accepted": data.get("accepted"),
        "modes": {
            "main": _as_bool(c.get("sync_main", True)),
            "extra": _as_bool(c.get("sync_extra", True)),
            "cf": _as_bool(c.get("sync_cf", False)),
        },
    }


@app.get("/api/cluster/import-preview")
async def api_cluster_import_preview(_=Depends(require_auth)):
    """روی مرکزی: همه URIهای نودها برای کپی/استفاده."""
    if _cluster_role() != "central":
        return {"lines": [], "count": 0}
    lines = []
    async with NODES_LOCK:
        for n in NODES.values():
            for cfg in n.get("configs") or []:
                uri = cfg.get("uri") if isinstance(cfg, dict) else str(cfg)
                if uri:
                    lines.append(uri)
    return {"lines": lines, "count": len(lines)}


# XHTTP router
try:
    from xhttp_siz10 import router as xhttp_router
    app.include_router(xhttp_router)
except Exception as _xhttp_err:
    logger.warning(f"XHTTP router not loaded: {_xhttp_err}")




# ── Plain path XHTTP: only if first segment is a known config path token ──────
class PlainPathXhttpMiddleware:
    """
    /r/{token}/... و /{token}/... → هندلر داخلی XHTTP
    مسیر کلاینت خنثی است (بدون نام پروتکل).
    """

    _SKIP = frozenset({
        "api", "login", "dashboard", "health", "healthz", "ready", "stats", "sub", "sub-all", "sub-group",
        "ws", "ss", "trojan-ws", "vless-tcp", "xhttp-siz10", "static", "assets", "docs",
        "openapi.json", "p", "proxy", "cf-sub", "domain-sub", "test-ws", "support",
        "cluster", "settings", "customers", "cloudflare", "connections", "traffic",
        "favicon.ico", "robots.txt", "admin", "metrics",
    })

    def __init__(self, app):
        self.app = app

    def _lookup_uid(self, token: str):
        if not token or token in self._SKIP:
            return None, None
        uid = PATH_INDEX.get(token)
        if not uid:
            if token in LINKS:
                uid = token
            else:
                for u, link in LINKS.items():
                    if str(link.get("path") or "").strip().strip("/") == token:
                        uid = u
                        break
        if not uid:
            return None, None
        link = LINKS.get(uid) or {}
        proto = str(link.get("protocol") or "")
        if "xhttp" not in proto:
            return None, None
        mode = "packet-up" if "packet" in proto else "stream-up"
        return uid, mode

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        path = scope.get("path") or ""
        if (not path) or path == "/" or path.startswith("/api") or path.startswith("/xhttp-siz10"):
            await self.app(scope, receive, send)
            return
        parts = [p for p in path.split("/") if p]
        if not parts:
            await self.app(scope, receive, send)
            return
        # پشتیبانی /r/{token}/... و /{token}/...
        if parts[0] == "r" and len(parts) >= 2:
            token = parts[1]
            rest = parts[2:]
        else:
            token = parts[0]
            rest = parts[1:]
            if token in self._SKIP:
                await self.app(scope, receive, send)
                return
        uid, mode = self._lookup_uid(token)
        if not uid:
            await self.app(scope, receive, send)
            return
        method = (scope.get("method") or "GET").upper()
        session_id = rest[0] if rest else "0"
        seq = rest[1] if len(rest) >= 2 else None
        if seq is not None and str(seq).isdigit():
            new_path = f"/xhttp-siz10/packet-up/{uid}/{session_id}/{seq}"
        elif method == "GET":
            new_path = f"/xhttp-siz10/{mode}/{uid}/{session_id}"
        else:
            if mode == "packet-up" and seq is not None and str(seq).isdigit():
                new_path = f"/xhttp-siz10/packet-up/{uid}/{session_id}/{seq}"
            else:
                new_path = f"/xhttp-siz10/{mode}/{uid}/{session_id}"
        scope = dict(scope)
        scope["path"] = new_path
        scope["raw_path"] = new_path.encode("utf-8")
        await self.app(scope, receive, send)


class VlessRootMiddleware:
    """
    Accept WebSocket on path=/ (Railway TCP Proxy sample style) without
    registering a FastAPI websocket route on "/" that can interfere with HTTP.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket" and scope.get("path") in ("/", ""):
            from starlette.websockets import WebSocket as StarletteWebSocket
            from relay_vless import websocket_tunnel_root
            ws = StarletteWebSocket(scope, receive, send)
            await websocket_tunnel_root(ws)
            return
        await self.app(scope, receive, send)


app.add_middleware(VlessRootMiddleware)
app.add_middleware(PlainPathXhttpMiddleware)

class SoftHeadersMiddleware:
    """حذف/خنثی‌سازی هدرهای شناسایی‌کننده."""
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = []
                for k, v in message.get("headers") or []:
                    lk = k.decode("latin-1").lower() if isinstance(k, bytes) else str(k).lower()
                    if lk in ("server", "x-powered-by"):
                        continue
                    headers.append((k, v))
                # generic
                headers.append((b"server", b"cloudflare"))
                message = {**message, "headers": headers}
            await send(message)
        await self.app(scope, receive, send_wrapper)

app.add_middleware(SoftHeadersMiddleware)





# ══════════════════════════════════════════════════════════════════════════════
# Telegram backup + alerts
# ══════════════════════════════════════════════════════════════════════════════

def _tg() -> dict:
    return SETTINGS.setdefault("telegram", {
        "bot_token": "", "admin_id": "", "backup_every_min": 10,
        "notify_quota": True, "notify_node_down": True, "enabled": False,
        "last_backup_at": "", "last_ok": False,
    })


async def telegram_send_message(text: str) -> dict:
    tg = _tg()
    token = str(tg.get("bot_token") or "").strip()
    admin = str(tg.get("admin_id") or "").strip()
    if not token or not admin:
        return {"ok": False, "detail": "bot_token یا admin_id خالی است"}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.post(url, json={
                "chat_id": admin,
                "text": text[:4000],
                "disable_web_page_preview": True,
            })
            data = r.json() if r.content else {}
            ok = bool(data.get("ok"))
            return {"ok": ok, "status": r.status_code, "data": data}
    except Exception as exc:
        return {"ok": False, "detail": str(exc)[:200]}


async def telegram_send_document(filename: str, content: bytes, caption: str = "") -> dict:
    tg = _tg()
    token = str(tg.get("bot_token") or "").strip()
    admin = str(tg.get("admin_id") or "").strip()
    if not token or not admin:
        return {"ok": False, "detail": "bot_token یا admin_id خالی است"}
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            files = {"document": (filename, content, "application/json")}
            data = {"chat_id": admin}
            if caption:
                data["caption"] = caption[:1000]
            r = await client.post(url, data=data, files=files)
            body = r.json() if r.content else {}
            return {"ok": bool(body.get("ok")), "status": r.status_code, "data": body}
    except Exception as exc:
        return {"ok": False, "detail": str(exc)[:200]}


def _build_backup_payload() -> dict:
    return {
        "version": get_current_panel_version(),
        "exported_at": datetime.now().isoformat(),
        "role": _cluster_role(),
        "host": get_host(),
        "links": dict(LINKS),
        "subs": dict(SUBS),
        "customers": dict(CUSTOMERS) if "CUSTOMERS" in globals() else {},
        "settings": {k: v for k, v in SETTINGS.items() if k != "telegram"},
        "nodes": dict(NODES),
        "auth_hint": "password_hash preserved — restore carefully",
        "auth": {"password_hash": AUTH.get("password_hash")},
    }


async def telegram_send_backup(reason: str = "auto") -> dict:
    import json as _json
    payload = _build_backup_payload()
    raw = _json.dumps(payload, ensure_ascii=False, indent=None).encode("utf-8")
    host = get_host() or "panel"
    fname = f"backup-{host.replace('/', '_')[:40]}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    caption = f"Backup ({reason})\nrole={_cluster_role()}\nhost={host}\nlinks={len(LINKS)} subs={len(SUBS)}"
    res = await telegram_send_document(fname, raw, caption=caption)
    tg = _tg()
    tg["last_backup_at"] = datetime.now().isoformat()
    tg["last_ok"] = bool(res.get("ok"))
    await save_state()
    return res


@app.get("/api/telegram/settings")
async def api_tg_settings_get(_=Depends(require_auth)):
    tg = dict(_tg())
    token = str(tg.get("bot_token") or "")
    tg["bot_token_set"] = bool(token)
    tg["bot_token_mask"] = (token[:6] + "…" + token[-4:]) if len(token) > 12 else ("***" if token else "")
    # never return full token
    tg.pop("bot_token", None)
    return tg


@app.post("/api/telegram/settings")
async def api_tg_settings_set(request: Request, _=Depends(require_auth)):
    body = await request.json()
    tg = _tg()
    if "bot_token" in body:
        val = str(body.get("bot_token") or "").strip()
        if val and val not in ("***", "unchanged"):
            tg["bot_token"] = val
    if "admin_id" in body:
        tg["admin_id"] = str(body.get("admin_id") or "").strip()
    if "backup_every_min" in body:
        try:
            tg["backup_every_min"] = max(5, min(1440, int(body.get("backup_every_min") or 10)))
        except Exception:
            tg["backup_every_min"] = 10
    for k in ("notify_quota", "notify_node_down", "enabled"):
        if k in body:
            tg[k] = bool(body.get(k))
    await save_state()
    # تست اتصال هنگام ذخیره اگر توکن و ایدی هست
    test = {"ok": False, "skipped": True}
    if tg.get("bot_token") and tg.get("admin_id"):
        test = await telegram_send_message(
            f"✅ اتصال تلگرام برقرار شد\nrole={_cluster_role()}\nhost={get_host()}\nبکاپ هر {tg.get('backup_every_min', 10)} دقیقه"
        )
        tg["enabled"] = bool(test.get("ok")) if body.get("enabled", True) else False
        tg["last_ok"] = bool(test.get("ok"))
        await save_state()
    return {"ok": True, "telegram": {k: v for k, v in tg.items() if k != "bot_token"}, "test": test}


@app.post("/api/telegram/test")
async def api_tg_test(_=Depends(require_auth)):
    res = await telegram_send_message(f"🔔 تست پنل\nrole={_cluster_role()}\nhost={get_host()}")
    return res


@app.post("/api/telegram/backup-now")
async def api_tg_backup_now(_=Depends(require_auth)):
    return await telegram_send_backup("manual")


@app.get("/api/backup/export")
async def api_backup_export(_=Depends(require_auth)):
    import json as _json
    payload = _build_backup_payload()
    raw = _json.dumps(payload, ensure_ascii=False, indent=2)
    return Response(
        content=raw,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="panel-backup-{datetime.now().strftime("%Y%m%d-%H%M")}.json"'},
    )


@app.post("/api/backup/restore")
async def api_backup_restore(request: Request, _=Depends(require_auth)):
    """بازیابی از JSON بکاپ (مراقب رمز و نودها باش)."""
    body = await request.json()
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="invalid backup")
    links = body.get("links") or {}
    subs = body.get("subs") or {}
    nodes = body.get("nodes") or {}
    settings = body.get("settings") or {}
    auth = body.get("auth") or {}
    if not isinstance(links, dict) or not isinstance(subs, dict):
        raise HTTPException(status_code=400, detail="backup missing links/subs")
    async with LINKS_LOCK:
        LINKS.clear()
        LINKS.update(links)
    async with SUBS_LOCK:
        SUBS.clear()
        SUBS.update(subs)
    async with NODES_LOCK:
        NODES.clear()
        NODES.update(nodes if isinstance(nodes, dict) else {})
    if isinstance(settings, dict):
        for k, v in settings.items():
            if k == "telegram":
                continue
            SETTINGS[k] = v
    if auth.get("password_hash"):
        AUTH["password_hash"] = auth["password_hash"]
    rebuild_path_index()
    await save_state()
    log_activity("backup", "بازیابی بکاپ انجام شد", "ok")
    return {"ok": True, "links": len(LINKS), "subs": len(SUBS), "nodes": len(NODES)}


async def _telegram_backup_loop():
    await asyncio.sleep(25)
    while True:
        try:
            tg = _tg()
            every = int(tg.get("backup_every_min") or 10)
            every = max(5, min(1440, every))
            if tg.get("enabled") and tg.get("bot_token") and tg.get("admin_id"):
                # فقط مرکزی یا standalone — نود معمولاً بکاپ سبک می‌فرستد
                if _cluster_role() in ("central", "standalone"):
                    await telegram_send_backup("auto")
            await asyncio.sleep(every * 60)
        except Exception as exc:
            logger.debug("tg backup loop: %s", exc)
            await asyncio.sleep(120)


# ══════════════════════════════════════════════════════════════════════════════
# Node health + sub failover
# ══════════════════════════════════════════════════════════════════════════════

async def _node_health_loop():
    await asyncio.sleep(20)
    while True:
        try:
            if _cluster_role() == "central":
                nh = SETTINGS.get("node_health") or {}
                interval = int(nh.get("interval_sec") or 120)
                async with NODES_LOCK:
                    items = [(nid, n.get("host") or "") for nid, n in NODES.items()]
                down_names = []
                for nid, host in items:
                    res = await _measure_node_ping(host)
                    async with NODES_LOCK:
                        if nid in NODES:
                            prev_ok = NODES[nid].get("last_ping_ok")
                            fails = int(NODES[nid].get("fail_count") or 0)
                            if res.get("ok"):
                                NODES[nid]["fail_count"] = 0
                                NODES[nid]["online"] = True
                            else:
                                fails += 1
                                NODES[nid]["fail_count"] = fails
                                NODES[nid]["online"] = fails < int(nh.get("fail_threshold") or 2)
                                if fails >= int(nh.get("fail_threshold") or 2):
                                    down_names.append(NODES[nid].get("name") or nid)
                            NODES[nid]["last_ping_ms"] = res.get("ms")
                            NODES[nid]["last_ping_ok"] = bool(res.get("ok"))
                            NODES[nid]["last_ping_at"] = datetime.now().isoformat()
                            if prev_ok and not res.get("ok") and fails >= int(nh.get("fail_threshold") or 2):
                                pass
                tg = _tg()
                if down_names and tg.get("enabled") and tg.get("notify_node_down"):
                    await telegram_send_message("⚠️ نودهای آفلاین:\n" + "\n".join(f"• {x}" for x in down_names[:20]))
                await asyncio.sleep(max(60, interval))
            else:
                await asyncio.sleep(90)
        except Exception as exc:
            logger.debug("node health loop: %s", exc)
            await asyncio.sleep(90)


def _node_is_online(node: dict) -> bool:
    if node.get("online") is False:
        return False
    if node.get("last_ping_ok") is False and int(node.get("fail_count") or 0) >= 2:
        return False
    return True


# ══════════════════════════════════════════════════════════════════════════════
# Emergency controls (node + central kill)
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/api/emergency/disable-all-local")
async def api_emergency_disable_all(_=Depends(require_auth)):
    """روی نود یا مرکزی: همه کانفیگ‌های محلی را غیرفعال می‌کند."""
    n = 0
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("active", True):
                link["active"] = False
                n += 1
    await save_state()
    log_activity("emergency", f"غیرفعال‌سازی اضطراری {n} کانفیگ محلی", "err")
    return {"ok": True, "disabled": n}


@app.post("/api/emergency/enable-all-local")
async def api_emergency_enable_all(_=Depends(require_auth)):
    n = 0
    async with LINKS_LOCK:
        for link in LINKS.values():
            if not link.get("active", True):
                link["active"] = True
                n += 1
    await save_state()
    return {"ok": True, "enabled": n}


@app.post("/api/emergency/disconnect-central")
async def api_emergency_disconnect_central(_=Depends(require_auth)):
    """روی نود: قطع ارتباط با مرکزی (دیگر sync/usage نمی‌فرستد)."""
    if _cluster_role() != "node":
        raise HTTPException(status_code=400, detail="فقط روی نود")
    c = _cluster()
    c["auto_sync"] = False
    c["central_url"] = ""
    # نگه داشتن token برای reconnect دستی
    await save_state()
    log_activity("cluster", "نود از مرکزی جدا شد (اضطراری)", "err")
    return {"ok": True}


@app.post("/api/cluster/control/kill-node")
async def api_cluster_kill_node(request: Request, _=Depends(require_auth)):
    """مرکزی → یک نود: disable_all روی همه کانفیگ‌های آن نود."""
    if _cluster_role() != "central":
        raise HTTPException(status_code=400, detail="فقط مرکزی")
    body = await request.json()
    node_id = str(body.get("node_id") or "")
    if not node_id:
        raise HTTPException(status_code=400, detail="node_id لازم است")
    ok = await _send_node_control(node_id, [], "disable_all", True)
    return {"ok": ok}


# extend control handler for disable_all / enable_all


@app.post("/api/links/import")
async def api_links_import(request: Request, _=Depends(require_auth)):
    """چسباندن چند URI (vless/trojan/ss) و ساخت کانفیگ محلی ساده."""
    body = await request.json()
    text = str(body.get("text") or body.get("uris") or "")
    sub_id = body.get("sub_id")
    lines = [ln.strip() for ln in text.replace(",", "\n").splitlines() if ln.strip()]
    created = []
    for ln in lines:
        if not (ln.startswith("vless://") or ln.startswith("trojan://") or ln.startswith("ss://")):
            continue
        try:
            from urllib.parse import urlparse, parse_qs, unquote
            proto = "vless-ws"
            label = "imported"
            path = secrets.token_urlsafe(8)
            if ln.startswith("vless://"):
                u = urlparse(ln)
                qs = parse_qs(u.query)
                typ = (qs.get("type") or ["ws"])[0]
                mode = (qs.get("mode") or [""])[0]
                if typ == "xhttp" or typ == "httpupgrade":
                    proto = f"xhttp-{mode}" if mode else "xhttp-stream-up"
                    if proto not in PROTOCOLS:
                        proto = "xhttp-stream-up"
                elif typ == "ws":
                    proto = "vless-ws"
                frag = unquote(u.fragment or "")
                if frag:
                    label = frag[:40]
                pth = (qs.get("path") or ["/"])[0]
                if pth and pth not in ("/",):
                    path = pth.strip("/").split("/")[-1][:32] or path
            elif ln.startswith("trojan://"):
                proto = "trojan-ws"
                u = urlparse(ln)
                frag = unquote(u.fragment or "")
                if frag:
                    label = frag[:40]
            else:
                proto = "shadowsocks-tls"
            uid = str(__import__("uuid").uuid4())
            path = await unique_config_path(path, uid[:8])
            link = {
                "label": label,
                "path": path,
                "protocol": proto,
                "active": True,
                "used_bytes": 0,
                "limit_bytes": 0,
                "created_at": datetime.now().isoformat(),
                "note": "imported",
                "sub_id": sub_id,
            }
            async with LINKS_LOCK:
                LINKS[uid] = link
            if sub_id:
                async with SUBS_LOCK:
                    if sub_id in SUBS:
                        ids = SUBS[sub_id].setdefault("link_ids", [])
                        if uid not in ids:
                            ids.append(uid)
            created.append({"uuid": uid, "label": label, "protocol": proto})
        except Exception as exc:
            logger.debug("import line fail: %s", exc)
    if created:
        rebuild_path_index()
        await save_state()
    return {"ok": True, "created": created, "count": len(created)}


@app.get("/api/templates/isp")
async def api_isp_templates(_=Depends(require_auth)):
    profiles = (SETTINGS.get("protocol_profiles") or {}).copy()
    defaults = {
        "general": ["trojan-ws", "vless-ws", "xhttp-stream-up"],
        "mobile": ["trojan-ws", "vless-ws", "shadowsocks-tls"],
        "mci": ["trojan-ws", "vless-ws"],
        "irancell": ["vless-ws", "trojan-ws", "xhttp-stream-up"],
        "wifi": ["xhttp-stream-up", "trojan-ws", "vless-ws"],
    }
    for k, v in defaults.items():
        profiles.setdefault(k, v)
    return {"templates": profiles}


@app.post("/api/templates/isp/apply")
async def api_isp_apply(request: Request, _=Depends(require_auth)):
    """برای یک ساب، فقط پروتکل‌های قالب ISP را در ساب نگه می‌دارد / اولویت می‌دهد."""
    body = await request.json()
    sub_id = str(body.get("sub_id") or "")
    template = str(body.get("template") or "general")
    profiles = SETTINGS.get("protocol_profiles") or {}
    wanted = list(profiles.get(template) or [])
    if not wanted:
        raise HTTPException(status_code=400, detail="template empty")
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        SUBS[sub_id]["isp_template"] = template
        SUBS[sub_id]["preferred_protocols"] = wanted
    await save_state()
    return {"ok": True, "template": template, "protocols": wanted}


def is_remote_link_eligible(link_id: str) -> bool:
    """برای ساب: اگر نود آفلاین است و sub_skip_offline فعال، رد کن."""
    nh = SETTINGS.get("node_health") or {}
    if not nh.get("sub_skip_offline", True):
        return True
    raw = str(link_id or "")
    if not raw.startswith("remote:"):
        return True
    parts = raw.split(":", 2)
    if len(parts) < 2:
        return True
    node = NODES.get(parts[1]) or {}
    return _node_is_online(node)




# ══════════════════════════════════════════════════════════════════════════════
# v4.8 — dual central, device limit, emergency token, quota TG, wizard helpers
# ══════════════════════════════════════════════════════════════════════════════

def _central_urls() -> list[str]:
    c = _cluster()
    urls = []
    for k in ("central_url", "central_url_secondary"):
        u = str(c.get(k) or "").strip().rstrip("/")
        if not u:
            continue
        if not u.startswith("http"):
            u = "https://" + u
        if u not in urls:
            urls.append(u)
    return urls


async def report_usage_to_central_multi(uuid: str, n_bytes: int) -> None:
    """گزارش مصرف به مرکزی؛ اگر اولی fail شد secondary را امتحان می‌کند."""
    if n_bytes <= 0 or _cluster_role() != "node":
        return
    c = _cluster()
    token = str(c.get("node_token") or "").strip()
    if not token:
        return
    urls = _central_urls()
    if not urls:
        return
    last_exc = None
    for central in urls:
        try:
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                r = await client.post(
                    f"{central}/api/cluster/usage",
                    headers={"X-Node-Token": token, "Authorization": f"Bearer {token}"},
                    json={"uuid": uuid, "source_id": uuid, "bytes": int(n_bytes)},
                )
            if r.status_code >= 400:
                last_exc = f"status {r.status_code}"
                continue
            data = r.json() if r.content else {}
            if data.get("allowed") is False:
                async with LINKS_LOCK:
                    if uuid in LINKS:
                        LINKS[uuid]["central_quota_exceeded"] = True
                await save_state()
            elif data.get("allowed") is True:
                async with LINKS_LOCK:
                    if uuid in LINKS and LINKS[uuid].get("central_quota_exceeded"):
                        LINKS[uuid]["central_quota_exceeded"] = False
            return
        except Exception as exc:
            last_exc = str(exc)
            continue
    logger.debug("report_usage multi failed: %s", last_exc)


# monkey-patch alias: prefer multi if original exists
try:
    report_usage_to_central = report_usage_to_central_multi  # type: ignore
except Exception:
    pass


def _sub_max_devices(sub: dict | None) -> int:
    if not sub:
        return 0
    try:
        return max(0, int(sub.get("max_devices") or 0))
    except Exception:
        return 0


def register_device_conn(sub_id: str | None, conn_key: str) -> bool:
    """True اگر زیر سقف دستگاه باشد یا سقف 0 (نامحدود)."""
    if not sub_id:
        return True
    sub = SUBS.get(sub_id)
    limit = _sub_max_devices(sub)
    if limit <= 0:
        return True
    s = DEVICE_CONN_INDEX.setdefault(sub_id, set())
    if conn_key in s:
        return True
    if len(s) >= limit:
        return False
    s.add(conn_key)
    return True


def unregister_device_conn(sub_id: str | None, conn_key: str) -> None:
    if not sub_id:
        return
    s = DEVICE_CONN_INDEX.get(sub_id)
    if not s:
        return
    s.discard(conn_key)
    if not s:
        DEVICE_CONN_INDEX.pop(sub_id, None)


@app.patch("/api/subs/{sub_id}/meta")
async def api_sub_meta(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        if "max_devices" in body:
            try:
                s["max_devices"] = max(0, int(body.get("max_devices") or 0))
            except Exception:
                pass
        if "tags" in body:
            tags = body.get("tags")
            if isinstance(tags, str):
                tags = [x.strip() for x in tags.split(",") if x.strip()]
            s["tags"] = list(tags or [])[:20]
        if "notes" in body:
            s["notes"] = str(body.get("notes") or "")[:500]
        if "preferred_protocols" in body:
            s["preferred_protocols"] = [str(x) for x in (body.get("preferred_protocols") or [])][:20]
    await save_state()
    return {"ok": True, "sub": SUBS.get(sub_id)}


# ── Emergency public token (no login) ──
def _emergency() -> dict:
    return SETTINGS.setdefault("emergency", {
        "path": "",
        "token": "",
        "created_at": "",
    })


@app.post("/api/emergency/public-token")
async def api_emergency_public_token(_=Depends(require_auth)):
    """ساخت path+token یکبارمصرف برای قطع اضطراری بدون لاگین."""
    path = secrets.token_urlsafe(12)
    token = secrets.token_urlsafe(24)
    em = _emergency()
    em["path"] = path
    em["token"] = token
    em["created_at"] = datetime.now().isoformat()
    await save_state()
    host = get_host()
    url = f"https://{host}/e/{path}?t={token}" if host else f"/e/{path}?t={token}"
    return {"ok": True, "path": path, "token": token, "url": url}


@app.post("/e/{path}")
@app.get("/e/{path}")
async def emergency_public_kill(path: str, request: Request):
    """بدون لاگین: اگر path و token درست باشد همه کانفیگ‌های محلی را قطع می‌کند."""
    em = _emergency()
    if not em.get("path") or path != em.get("path"):
        raise HTTPException(status_code=404, detail="not found")
    tkn = request.query_params.get("t") or request.headers.get("x-emergency-token") or ""
    if not tkn or tkn != em.get("token"):
        raise HTTPException(status_code=404, detail="not found")
    n = 0
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("active", True):
                link["active"] = False
                n += 1
    # invalidate token after use (one-time)
    em["token"] = ""
    em["path"] = ""
    await save_state()
    log_activity("emergency", f"قطع اضطراری عمومی: {n} کانفیگ", "err")
    try:
        if _tg().get("enabled"):
            await telegram_send_message(f"🚨 قطع اضطراری عمومی\nhost={get_host()}\ndisabled={n}")
    except Exception:
        pass
    return {"ok": True, "disabled": n, "message": "all local configs disabled"}


@app.post("/api/cluster/nodes/{node_id}/kill")
async def api_node_kill(node_id: str, _=Depends(require_auth)):
    if _cluster_role() != "central":
        raise HTTPException(status_code=400, detail="فقط مرکزی")
    ok = await _send_node_control(node_id, [], "disable_all", True)
    try:
        if _tg().get("enabled"):
            await telegram_send_message(f"🛑 Kill نود از مرکزی\nnode={node_id}\nok={ok}")
    except Exception:
        pass
    return {"ok": ok, "node_id": node_id}


# ── Protocol priority when collecting sub lines ──
_ORIG_COLLECT = None

def _sort_lines_by_protocol_pref(lines: list[str], preferred: list[str]) -> list[str]:
    if not preferred or not lines:
        return lines
    def score(uri: str) -> int:
        u = uri.lower()
        for i, p in enumerate(preferred):
            p = p.lower()
            if "xhttp" in p and "xhttp" in u:
                return i
            if "trojan" in p and u.startswith("trojan://"):
                return i
            if "vless" in p and u.startswith("vless://"):
                return i
            if "shadow" in p and u.startswith("ss://"):
                return i
        return 100
    return sorted(lines, key=score)


# wrap collect after definition - patch at runtime in startup
async def _quota_notify_loop():
    await asyncio.sleep(40)
    while True:
        try:
            tg = _tg()
            if tg.get("enabled") and tg.get("notify_quota", True) and _cluster_role() in ("central", "standalone"):
                async with SUBS_LOCK:
                    items = list(SUBS.items())
                for sid, s in items:
                    lim = 0
                    try:
                        lim = int(s.get("limit_bytes") or 0)
                    except Exception:
                        lim = 0
                    used = int(s.get("used_bytes") or 0)
                    if lim > 0:
                        pct = used / lim * 100
                        flags = s.setdefault("_notify_flags", {})
                        if pct >= 100 and not flags.get("100"):
                            flags["100"] = True
                            await telegram_send_message(f"🔴 سهمیه تمام شد\nsub={s.get('name') or sid}")
                        elif pct >= 90 and not flags.get("90"):
                            flags["90"] = True
                            await telegram_send_message(f"🟠 سهمیه ۹۰٪\nsub={s.get('name') or sid}\n{pct:.0f}%")
                        elif pct >= 70 and not flags.get("70"):
                            flags["70"] = True
                            await telegram_send_message(f"🟡 سهمیه ۷۰٪\nsub={s.get('name') or sid}\n{pct:.0f}%")
                    # expiry
                    exp = s.get("expires_at") or s.get("expire_at")
                    if exp:
                        try:
                            from datetime import datetime as _dt
                            if isinstance(exp, (int, float)):
                                exp_dt = _dt.fromtimestamp(exp)
                            else:
                                exp_dt = _dt.fromisoformat(str(exp).replace("Z", ""))
                            days = (exp_dt - _dt.now()).days
                            flags = s.setdefault("_notify_flags", {})
                            if days <= 0 and not flags.get("exp0"):
                                flags["exp0"] = True
                                await telegram_send_message(f"🔴 انقضای اشتراک\nsub={s.get('name') or sid}")
                            elif days <= 3 and not flags.get("exp3"):
                                flags["exp3"] = True
                                await telegram_send_message(f"🟠 انقضا تا {days} روز\nsub={s.get('name') or sid}")
                        except Exception:
                            pass
            await asyncio.sleep(600)
        except Exception as exc:
            logger.debug("quota notify: %s", exc)
            await asyncio.sleep(300)


async def _central_watchdog_loop():
    """روی نود: اگر مرکزی ۲۴ساعت جواب ندهد به تلگرام خبر بده."""
    await asyncio.sleep(60)
    while True:
        try:
            if _cluster_role() == "node":
                c = _cluster()
                token = str(c.get("node_token") or "")
                urls = _central_urls()
                ok_any = False
                for central in urls:
                    try:
                        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                            r = await client.get(f"{central}/health")
                            if r.status_code < 500:
                                ok_any = True
                                c["last_central_ok_at"] = datetime.now().isoformat()
                                break
                    except Exception:
                        continue
                if not ok_any and urls:
                    last = c.get("last_central_ok_at")
                    stale = True
                    if last:
                        try:
                            last_dt = datetime.fromisoformat(str(last))
                            stale = (datetime.now() - last_dt).total_seconds() > 86400
                        except Exception:
                            stale = True
                    else:
                        # first fail — set timestamp and wait
                        c["last_central_ok_at"] = datetime.now().isoformat()
                        stale = False
                    if stale and not c.get("_central_down_notified"):
                        c["_central_down_notified"] = True
                        await save_state()
                        # local telegram might not be configured on node; try anyway
                        await telegram_send_message(
                            f"⚠️ مرکزی بیش از ۲۴ ساعت در دسترس نیست\nnode={c.get('node_name')}\nhost={get_host()}"
                        )
                elif ok_any:
                    c["_central_down_notified"] = False
            await asyncio.sleep(3600)
        except Exception as exc:
            logger.debug("central watchdog: %s", exc)
            await asyncio.sleep(1800)


# ── Rate limit new tunnel connections ──
_CONN_RATE: dict = {}
_CONN_RATE_WINDOW = 10.0
_CONN_RATE_MAX = 40  # per IP per window


def allow_new_connection(ip: str) -> bool:
    import time as _time
    now = _time.time()
    bucket = _CONN_RATE.setdefault(ip or "unknown", [])
    bucket[:] = [t for t in bucket if now - t < _CONN_RATE_WINDOW]
    if len(bucket) >= _CONN_RATE_MAX:
        return False
    bucket.append(now)
    return True


@app.get("/api/cluster/wizard-status")
async def api_wizard_status(_=Depends(require_auth)):
    """وضعیت برای ویزارد بازیابی بعد از بن."""
    c = _cluster()
    tg = _tg()
    async with NODES_LOCK:
        nodes = len(NODES)
        online = sum(1 for n in NODES.values() if n.get("last_ping_ok"))
    return {
        "role": _cluster_role(),
        "has_secret": bool(c.get("cluster_secret")),
        "nodes": nodes,
        "online": online,
        "telegram_ok": bool(tg.get("last_ok")),
        "telegram_enabled": bool(tg.get("enabled")),
        "links": len(LINKS),
        "subs": len(SUBS),
        "steps": [
            {"id": "restore", "title": "بازیابی بکاپ JSON", "done": len(SUBS) > 0 or len(LINKS) > 0},
            {"id": "secret", "title": "ساخت Cluster Secret", "done": bool(c.get("cluster_secret"))},
            {"id": "telegram", "title": "اتصال تلگرام", "done": bool(tg.get("enabled") and tg.get("last_ok"))},
            {"id": "nodes", "title": "اتصال مجدد نودها", "done": nodes > 0},
        ],
    }


@app.post("/api/backup/restore-upload")
async def api_backup_restore_upload(request: Request, _=Depends(require_auth)):
    body = await request.json()
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="invalid backup")
    # reuse logic
    links = body.get("links") or {}
    subs = body.get("subs") or {}
    nodes = body.get("nodes") or {}
    settings = body.get("settings") or {}
    auth = body.get("auth") or {}
    if not isinstance(links, dict) or not isinstance(subs, dict):
        raise HTTPException(status_code=400, detail="backup missing links/subs")
    async with LINKS_LOCK:
        LINKS.clear()
        LINKS.update(links)
    async with SUBS_LOCK:
        SUBS.clear()
        SUBS.update(subs)
    async with NODES_LOCK:
        NODES.clear()
        NODES.update(nodes if isinstance(nodes, dict) else {})
    if isinstance(settings, dict):
        for k, v in settings.items():
            if k == "telegram":
                continue
            SETTINGS[k] = v
    if auth.get("password_hash"):
        AUTH["password_hash"] = auth["password_hash"]
    rebuild_path_index()
    await save_state()
    log_activity("backup", "بازیابی بکاپ از آپلود", "ok")
    return {"ok": True, "links": len(LINKS), "subs": len(SUBS), "nodes": len(NODES)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
