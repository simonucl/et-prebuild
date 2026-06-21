FROM ubuntu:22.04

LABEL Author="Container for cron-file creation exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/docs

RUN cat > /home/user/docs/generate_docs.sh <<'EOF'
#!/usr/bin/env bash
# Dummy implementation for test scaffolding
echo "Generating documentation…"
EOF

RUN chmod 755 /home/user/docs/generate_docs.sh && \
    chmod 755 /home/user/docs

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    chown -R user:user /home/user