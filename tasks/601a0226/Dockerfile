FROM ubuntu:22.04

# Labels
LABEL Author="education-bot"
LABEL Description="Base image for Cron scheduling exercise"

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create the build directory and required shell scripts
RUN mkdir -p /home/user/build

RUN cat >/home/user/build/build_android.sh <<'EOF'
#!/usr/bin/env bash
echo "Building Android..."
EOF

RUN cat >/home/user/build/cleanup_artifacts.sh <<'EOF'
#!/usr/bin/env bash
echo "Cleaning up old artefacts..."
EOF

RUN chmod 755 /home/user/build/build_android.sh /home/user/build/cleanup_artifacts.sh && \
    chmod 755 /home/user && \
    chmod 755 /home/user/build && \
    rm -f /var/spool/cron/crontabs/* || true