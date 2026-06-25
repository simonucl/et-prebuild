# Configure the Release Console NGINX Site

You are preparing an offline NGINX container for a release-console smoke test. Static content is already staged under `/srv`; do not edit, copy, move, rename, or delete anything under `/srv`.

Create and enable a site named `release-console` using these exact paths:

- Main site config: `/etc/nginx/sites-available/release-console.conf`
- Enabled site link: `/etc/nginx/sites-enabled/release-console.conf`

The enabled-site entry must be a symbolic link to the file in `sites-available`. Disable the packaged/default site by removing `/etc/nginx/sites-enabled/default` if it exists.

The new server must:

- Listen on port `18082` as the `default_server`.
- Serve the current release rooted at `/srv/releases/current/public`.
- Include `/etc/nginx/snippets/hardened_headers.conf` at server scope.
- Ensure the hardened headers are still present on successful responses from locations that define their own headers.
- For `/`, serve normal files and directories and fall back to `/index.html` for application routes.
- For `/app/`, serve normal files and directories under the release root and fall back to `/app/index.html` for nested application routes.
- For `/assets/`, use NGINX `alias` to expose `/srv/releases/current/public/assets/`, return `404` for missing asset files, add `Cache-Control: public, max-age=31536000, immutable`, and serve existing precompressed `.gz` files when the client advertises gzip support.
- For `/exports/`, use NGINX `alias` to expose `/srv/shared/exports/`, keep directory listing disabled, return `404` for missing files, and add `Cache-Control: private, no-store`.
- For the exact path `/api/status`, return JSON exactly as `{"status":"ok","release":"2026.06"}` followed by a newline, with an `application/json` content type.
- Return `404` for other paths below `/api/`.
- Configure `/maintenance.html` as an internal-only maintenance error page backed by `/srv/shared/errors/maintenance.html`.
- Configure the exact path `/force-maintenance` to return `503` using that internal maintenance page.

When you are finished, `nginx -t` should pass, and starting NGINX should make the site work on `http://127.0.0.1:18082/`.
