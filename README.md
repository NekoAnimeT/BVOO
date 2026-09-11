# OXNET Edge Console

Edge delivery control panel for managing traffic routes, subscription endpoints,
domain mappings (including Cloudflare clean addresses), and bandwidth analytics.

## Features
- Light / dark professional UI
- Multi-route configuration management
- Subscription groups and public pages
- Main domain, Cloudflare domains, and secondary domains
- Clean IP / hostname lists for edge routes
- Persistent state via Volume (`/data` or `DATA_DIR`)
- Remark templates and subscription info lines

## Deploy notes (Railway)
1. Mount a Volume at `/data` (or set `DATA_DIR`) so state survives redeploys.
2. Expose the application HTTP port from the `PORT` environment variable.
3. Optional: configure a public TCP route and enter host/port in Settings.

## Health
- `GET /` — service metadata
- `GET /health` or `/healthz` — liveness

This project is framed as an **edge / CDN delivery console**, not a consumer VPN product.
