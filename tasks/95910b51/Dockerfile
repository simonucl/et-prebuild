FROM ubuntu:22.04

# Help section
# This container image provides the initial filesystem layout required for the
# migration task and includes pytest for automated grading.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/migration/source_configs && \
    mkdir -p /home/user/migration/archives && \
    mkdir -p /home/user/migration/restore

RUN cat <<'EOF' > /home/user/migration/source_configs/config1.conf
server_name=alpha
port=8080
EOF

RUN cat <<'EOF' > /home/user/migration/source_configs/config2.conf
server_name=beta
port=9090
EOF

RUN chmod -R 777 /home/user

# Labels
LABEL Author="Cloud-Architecture Task Setup"
LABEL Description="Environment prepared for migration-archive exercise with pytest pre-installed."