#!/bin/bash
set -euo pipefail

mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
rm -f /etc/nginx/sites-enabled/default

cat > /etc/nginx/sites-available/release-console.conf <<'NGINX'
server {
    listen 18082 default_server;
    server_name _;

    root /srv/releases/current/public;
    index index.html;

    include /etc/nginx/snippets/hardened_headers.conf;
    error_page 503 /maintenance.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /app/ {
        try_files $uri $uri/ /app/index.html;
    }

    location /assets/ {
        alias /srv/releases/current/public/assets/;
        gzip_static on;
        try_files $uri =404;
        add_header Cache-Control "public, max-age=31536000, immutable" always;
        include /etc/nginx/snippets/hardened_headers.conf;
    }

    location /exports/ {
        alias /srv/shared/exports/;
        autoindex off;
        try_files $uri =404;
        add_header Cache-Control "private, no-store" always;
        include /etc/nginx/snippets/hardened_headers.conf;
    }

    location = /api/status {
        default_type application/json;
        return 200 '{"status":"ok","release":"2026.06"}\n';
    }

    location /api/ {
        return 404;
    }

    location = /maintenance.html {
        internal;
        alias /srv/shared/errors/maintenance.html;
    }

    location = /force-maintenance {
        return 503;
    }
}
NGINX

ln -s /etc/nginx/sites-available/release-console.conf /etc/nginx/sites-enabled/release-console.conf
nginx -t
