# This container sets up the initial state for the "build configuration update" exercise and includes pytest for automated validation.
FROM ubuntu:22.04

ENV PATH="$PATH:/root/.local/bin"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/build_configs && \
    chmod 755 /home/user/build_configs

RUN cat > /home/user/build_configs/app.yaml <<'EOF'
name: sample-app
version: "1.2.3"
EOF

RUN chmod 644 /home/user/build_configs/app.yaml

RUN cat > /home/user/build_configs/release.toml <<'EOF'
[build]
number = 102

[metadata]
checksum = ""
EOF

RUN chmod 644 /home/user/build_configs/release.toml