FROM nginx:1.27-bookworm

RUN mkdir -p /home/user /srv/docs/current /srv/docs/releases/2026.06.28/assets \
    && chmod 755 /home/user

RUN printf '%s\n' \
    '<!doctype html>' \
    '<html>' \
    '  <head><title>Docs Portal</title></head>' \
    '  <body>DOCS_PORTAL_CURRENT_BUILD=2026.06.28</body>' \
    '</html>' \
    > /srv/docs/current/index.html

RUN printf '%s\n' 'docs portal static health ok' > /srv/docs/current/health.txt

RUN printf '%s\n' 'window.__DOCS_ASSET_BUILD__ = "2026.06.28";' \
    > /srv/docs/releases/2026.06.28/assets/app.abc123.js

RUN printf '%s\n' 'release-root-secret-must-not-be-served' \
    > /srv/docs/releases/2026.06.28/secret.txt

RUN rm -f /etc/nginx/conf.d/default.conf \
    && printf '%s\n' \
      'server {' \
      '    listen 9000;' \
      '    server_name _;' \
      '' \
      '    location / {' \
      '        default_type text/plain;' \
      '        return 200 "UPSTREAM_PATH=$request_uri\n";' \
      '    }' \
      '}' \
      > /etc/nginx/conf.d/upstream_echo.conf

RUN printf '%s\n' \
    'server {' \
    '    listen 18080 default_server;' \
    '    server_name _;' \
    '' \
    '    root /srv/docs/releases/2026.06.28;' \
    '    index index.html;' \
    '' \
    '    location / {' \
    '        try_files $uri $uri/ =404;' \
    '    }' \
    '' \
    '    location /assets/ {' \
    '        root /srv/docs/current;' \
    '        expires 1y;' \
    '    }' \
    '' \
    '    location /api/ {' \
    '        proxy_pass http://127.0.0.1:9000;' \
    '    }' \
    '}' \
    > /etc/nginx/conf.d/docs-portal.conf

WORKDIR /home/user
CMD ["bash"]
