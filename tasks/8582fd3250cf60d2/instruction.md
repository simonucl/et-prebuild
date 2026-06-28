# Repair the Docs Portal NGINX Migration

You are finishing a static-docs migration on an isolated host. The host already contains a broken NGINX site at:

`/etc/nginx/conf.d/docs-portal.conf`

There is also an internal test upstream already configured at `127.0.0.1:9000`. Do not modify `/etc/nginx/conf.d/upstream_echo.conf`.

Repair the configuration and leave a short machine-readable migration report.

## Required NGINX behavior

The final NGINX configuration must:

1. Listen on port `18080` as the default server.
2. Serve the current single-page documentation app from `/srv/docs/current`.
   - `/` must return `/srv/docs/current/index.html`.
   - Existing files under `/srv/docs/current`, such as `/health.txt`, must be served normally.
   - Unknown non-asset paths such as `/guide/install/linux` must fall back to `/srv/docs/current/index.html`.
3. Serve release assets from `/srv/docs/releases/2026.06.28/assets/` under the URL prefix `/assets/`.
   - Use NGINX path mapping appropriate for a URL prefix that points into a different filesystem directory.
   - Add a `Cache-Control` response header containing `public`, `max-age=31536000`, and `immutable` for asset responses.
   - Do not expose files from the release root outside the `assets` directory.
4. Proxy `/api/...` requests to `http://127.0.0.1:9000/...` with the `/api/` prefix stripped before forwarding.
   - For example, `/api/status?check=ready` must reach the upstream as `/status?check=ready`.
5. Pass `nginx -t`.

Do not modify files under `/srv/docs`.

## Migration Report

Create `/home/user/nginx_migration_report.json` as minified JSON with exactly these keys in this order:

```json
{"site":"docs-portal","listen":18080,"spa_root":"/srv/docs/current","asset_alias":"/srv/docs/releases/2026.06.28/assets/","api_upstream":"http://127.0.0.1:9000/","validation_command":"nginx -t"}
```

The report should end with a single trailing newline.
