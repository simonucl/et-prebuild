# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && mkdir -p /home/user/resources

RUN cat > /home/user/logs/dns_failures.log <<'EOF'
app.internal.local
db.internal.local
cache.internal.local
auth.service
gateway.service
EOF

RUN cat > /home/user/resources/hosts_override <<'EOF'
10.0.0.11 app.internal.local
10.0.0.12 db.internal.local
10.0.0.13 cache.internal.local
EOF

RUN chmod 755 /home && chmod -R 755 /home/user && chmod 644 /home/user/logs/dns_failures.log && chmod 644 /home/user/resources/hosts_override

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1