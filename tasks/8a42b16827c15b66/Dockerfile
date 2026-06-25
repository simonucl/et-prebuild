FROM nginx:1.27-bookworm

WORKDIR /app

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends bash curl gzip ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled /etc/nginx/snippets; \
    if ! grep -q '/etc/nginx/sites-enabled' /etc/nginx/nginx.conf; then \
      sed -i '/include \/etc\/nginx\/conf.d\/\*.conf;/a\    include /etc/nginx/sites-enabled/*.conf;' /etc/nginx/nginx.conf; \
    fi; \
    rm -f /etc/nginx/conf.d/default.conf; \
    printf '%s\n' \
      'server {' \
      '    listen 18082 default_server;' \
      '    server_name _;' \
      '    return 444;' \
      '}' \
      > /etc/nginx/sites-available/default; \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default; \
    printf '%s\n' \
      'add_header X-Frame-Options "DENY" always;' \
      'add_header X-Content-Type-Options "nosniff" always;' \
      'add_header Referrer-Policy "strict-origin-when-cross-origin" always;' \
      > /etc/nginx/snippets/hardened_headers.conf; \
    mkdir -p /srv/releases/2026.05/public/app \
             /srv/releases/2026.06/public/app \
             /srv/releases/2026.06/public/assets \
             /srv/releases/2026.06/public/docs \
             /srv/shared/exports \
             /srv/shared/errors \
             /home/user; \
    printf '%s\n' '<!doctype html><title>old console</title><h1>Release Console 2026.05</h1>' > /srv/releases/2026.05/public/index.html; \
    printf '%s\n' '<!doctype html><title>release console</title><h1>Release Console 2026.06</h1>' > /srv/releases/2026.06/public/index.html; \
    printf '%s\n' '<!doctype html><title>release app</title><main id="app">Release app shell 2026.06</main>' > /srv/releases/2026.06/public/app/index.html; \
    printf '%s\n' 'console.log("release-console build 77f3");' > /srv/releases/2026.06/public/assets/main.77f3.js; \
    gzip -n -9 -c /srv/releases/2026.06/public/assets/main.77f3.js > /srv/releases/2026.06/public/assets/main.77f3.js.gz; \
    printf '%s\n' 'body{font-family:system-ui;color:#1d2939}' > /srv/releases/2026.06/public/assets/main.77f3.css; \
    printf '%s\n' 'runbook: promote only after smoke checks pass' > /srv/releases/2026.06/public/docs/runbook.txt; \
    printf '%s\n' 'day,status' '2026-06-25,green' > /srv/shared/exports/daily.csv; \
    printf '%s\n' '<!doctype html><title>maintenance</title><h1>Release maintenance window</h1>' > /srv/shared/errors/maintenance.html; \
    ln -sfn /srv/releases/2026.06 /srv/releases/current; \
    chmod -R a+rX /srv

CMD ["bash"]
