FROM ubuntu:22.04

# %help not provided in source

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/projects/myapp/config

RUN cat >/home/user/projects/myapp/config/app.conf <<'EOF'
APP_ENV=production
EOF

RUN cat >/home/user/projects/myapp/config/db.conf <<'EOF'
DB_HOST=localhost
EOF

RUN cat >/home/user/projects/myapp/config/secrets.conf <<'EOF'
API_KEY=demo123
EOF

RUN chmod 755 /home/user /home/user/projects /home/user/projects/myapp /home/user/projects/myapp/config && \
    chmod 644 /home/user/projects/myapp/config/*.conf

RUN apt-get clean && rm -rf /var/lib/apt/lists/*