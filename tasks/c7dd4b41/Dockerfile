FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app

RUN cat > /home/user/app/Dockerfile <<'EOF'
FROM alpine:latest

CMD ["echo", "Hello World"]
EOF

RUN chmod 644 /home/user/app/Dockerfile && \
    chmod -R a+rX /home/user && \
    chmod -R a+w /home/user

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:$PATH