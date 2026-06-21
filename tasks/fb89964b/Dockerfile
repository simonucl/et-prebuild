FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/support && \
    chmod 0777 /home/user/support && \
    touch /home/user/support/firmware_v2.1.0.bin && \
    chmod 0644 /home/user/support/firmware_v2.1.0.bin

RUN cat <<'EOF' > /home/user/support/reference.sha256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  firmware_v2.1.0.bin
EOF

RUN chmod 0644 /home/user/support/reference.sha256

CMD ["bash"]