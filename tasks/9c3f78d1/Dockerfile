FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN mkdir -p /home/user/artifacts_staging

RUN printf 'appcli binary for x86_64 version 2.3.0\n' \
        > /home/user/artifacts_staging/appcli-2.3.0-linux-x86_64.bin

RUN printf 'appcli binary for arm64 version 2.3.0\n' \
        > /home/user/artifacts_staging/appcli-2.3.0-linux-arm64.bin

RUN cat > /home/user/artifacts_staging/CHANGELOG-2.3.0.md <<'EOF'
# Changelog for v2.3.0

- Feature A
- Bug fix B
EOF

RUN chmod 0777 /home/user/artifacts_staging && \
    chmod 0666 /home/user/artifacts_staging/*

RUN rm -rf /home/user/releases

# Environment modifications
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH