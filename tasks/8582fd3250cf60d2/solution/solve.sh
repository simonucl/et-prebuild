#!/bin/bash
set -euo pipefail

cat > /etc/nginx/conf.d/docs-portal.conf <<'EOF'
server {
    listen 18080 default_server;
    server_name _;

    root /srv/docs/current;
    index index.html;

    location /assets/ {
        alias /srv/docs/releases/2026.06.28/assets/;
        add_header Cache-Control "public, max-age=31536000, immutable";
        try_files $uri =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:9000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF

rm -f /etc/nginx/conf.d/default.conf
printf '%s\n' '{"site":"docs-portal","listen":18080,"spa_root":"/srv/docs/current","asset_alias":"/srv/docs/releases/2026.06.28/assets/","api_upstream":"http://127.0.0.1:9000/","validation_command":"nginx -t"}' > /home/user/nginx_migration_report.json

nginx -t
