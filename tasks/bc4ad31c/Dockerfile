# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Equivalent of %post
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -s /bin/bash user; fi

RUN mkdir -p /home/user/secure_app && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/secure_app

RUN cat <<'EOF' > /home/user/secure_app/config.ini
[credentials]
API_KEY = OLDKEY-12345
EOF

RUN chmod 0644 /home/user/secure_app/config.ini && \
    chown -R 1000:1000 /home/user/secure_app

# Equivalent of %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8

# Equivalent of %runscript
CMD ["bash", "-c", "\"$@\""]