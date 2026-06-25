FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    coreutils \
    curl \
    gzip \
    nginx \
    python3 \
    tar \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    useradd -m -s /bin/bash user; \
    mkdir -p /srv/releases/2026.06/public/assets \
             /srv/releases/2026.06/public/docs \
             /srv/shared/reports \
             /srv/shared/errors \
             /etc/nginx/snippets \
             /etc/nginx/sites-available \
             /etc/nginx/sites-enabled \
             /home/user/site/handoff; \
    ln -s /srv/releases/2026.06 /srv/releases/current; \
    printf '%s\n' \
      '<!doctype html>' \
      '<html><head><title>Support Console</title><link rel="stylesheet" href="/static/app.css"></head><body><main id="app">Support Console 2026.06</main><script src="/static/app.js"></script></body></html>' \
      > /srv/releases/2026.06/public/index.html; \
    printf '%s\n' ':root { color-scheme: light; } body { font-family: sans-serif; margin: 2rem; }' \
      > /srv/releases/2026.06/public/assets/app.css; \
    printf '%s\n' 'document.querySelector("#app").dataset.release = "2026.06";' \
      > /srv/releases/2026.06/public/assets/app.js; \
    printf '%s\n' '<!doctype html><html><body><h1>Runbook</h1><p>Escalation path: support-console.</p></body></html>' \
      > /srv/releases/2026.06/public/docs/runbook.html; \
    printf '%s\n' 'team,open_tickets' 'alpha,7' 'bravo,3' \
      > /srv/shared/reports/usage.csv; \
    printf '%s\n' '<!doctype html><html><body><h1>Maintenance</h1></body></html>' \
      > /srv/shared/errors/maintenance.html; \
    ln -s app.css /srv/releases/2026.06/public/assets/current.css; \
    printf '%s\n' \
      'add_header X-Frame-Options "DENY" always;' \
      'add_header X-Content-Type-Options "nosniff" always;' \
      'add_header Referrer-Policy "no-referrer" always;' \
      > /etc/nginx/snippets/support_security_headers.conf; \
    rm -f /etc/nginx/sites-enabled/default; \
    chown -R user:user /home/user/site; \
    chmod -R a+rX /srv
