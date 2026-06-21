# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# --- %post section ---
RUN set -e && \
    groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    mkdir -p /home/user/services/webapp

RUN cat > /home/user/services/webapp/app.conf <<'EOF'
PORT=8080
DEBUG=False
EOF

RUN cat > /home/user/services/webapp/restart.sh <<'EOF'
#!/bin/bash
echo "Webapp restarted on port $(grep '^PORT' "$(dirname "$0")/app.conf" | cut -d'=' -f2)"
EOF

RUN chmod +x /home/user/services/webapp/restart.sh

RUN set -e && \
    chown -R 1000:1000 /home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- %environment section ---
ENV HOME=/home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN chmod 755 /home/user

# --- %runscript equivalent ---
CMD ["/bin/bash"]