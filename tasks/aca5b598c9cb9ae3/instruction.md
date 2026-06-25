# Support Console NGINX Snapshot

You are preparing an offline support-console container for a smoke test and an air-gapped handoff.

Do not edit, copy, move, or delete anything under `/srv`. The current release is already staged at `/srv/releases/current/public`, shared reports are under `/srv/shared/reports`, and a maintenance page is under `/srv/shared/errors/maintenance.html`.

## NGINX site

Create and enable a site named `support-console` using these exact paths:

- Main config: `/etc/nginx/sites-available/support-console.conf`
- Enabled config: `/etc/nginx/sites-enabled/support-console.conf`

The enabled config must be a symbolic link to the file in `sites-available`. Remove `/etc/nginx/sites-enabled/default` if it exists.

The server must:

- Listen on port `18082` as the `default_server`.
- Serve the console under the `/console/` URL prefix from `/srv/releases/current/public/`.
- For `/console/`, serve real files and directories when present, and fall back to `/console/index.html` for application routes.
- Expose `/static/` with NGINX `alias` from `/srv/releases/current/public/assets/`, return `404` for missing static files, and add `Cache-Control: public, max-age=31536000, immutable`.
- Expose `/reports/` with NGINX `alias` from `/srv/shared/reports/`, keep directory listing disabled, return `404` for missing report files, and add `Cache-Control: private, no-store`.
- Include `/etc/nginx/snippets/support_security_headers.conf` at server scope, and make sure the same security headers are also present on successful responses from locations that define their own headers.
- For the exact path `/readyz`, return plain text `ok` followed by a newline.
- Configure `/maintenance.html` as an internal-only maintenance page backed by `/srv/shared/errors/maintenance.html`; a direct browser request to `/maintenance.html` must not return the page.

`nginx -t` must pass, and starting NGINX must make the site work at `http://127.0.0.1:18082/console/`.

## Handoff bundle

Replace any stale contents of `/home/user/site/handoff` with exactly these files:

- `/home/user/site/handoff/support-console-snapshot.tar.gz`
- `/home/user/site/handoff/manifest.json`
- `/home/user/site/handoff/SHA256SUMS`

The gzip stream for `support-console-snapshot.tar.gz` must be deterministic: gzip mtime zero and no stored original filename. The tar archive inside it must use mtime `1800000000`, numeric owner/group `0/0`, directories mode `0755`, regular files mode `0644`, and sorted member order. It must contain one root directory, `support-console/`, with:

- `config/support-console.conf`, byte-for-byte matching the enabled site config target.
- `config/enabled.conf`, a symlink to `support-console.conf`.
- `public/index.html`, `public/assets/app.css`, `public/assets/app.js`, `public/assets/current.css`, and `public/docs/runbook.html` from the staged current release. Preserve `public/assets/current.css` as a symlink to `app.css`.

Write `manifest.json` as one minified JSON line ending in exactly one newline. Its top-level keys, in order, must be `bundle`, `generated_at`, `members`, and `archive_sha256`.

- `bundle` is `support-console-snapshot.tar.gz`.
- `generated_at` is `2026-06-25T00:00:00Z`.
- `members` lists every tar member in archive order. Each entry must contain `path`, `type`, `mode`, `bytes`, and `sha256` in that order. Use `type` values `dir`, `file`, or `symlink`; directories and symlinks have empty SHA256 and size `0`.
- `archive_sha256` is the SHA256 digest of `support-console-snapshot.tar.gz`.

Write `SHA256SUMS` with exactly two lines:

```text
<sha256 of support-console-snapshot.tar.gz>  support-console-snapshot.tar.gz
<sha256 of manifest.json>  manifest.json
```

All work must be completed without network access.
