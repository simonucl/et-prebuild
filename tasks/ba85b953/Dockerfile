# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author your_name_here
# Container prepared for the “security scan” CLI task.
# Contains:
#   - /home/user/scripts with three example shell scripts
#   - pytest installed for automated testing

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/scripts

RUN cat > /home/user/scripts/backup.sh <<'EOF'
#!/bin/bash
# Daily backup script
password="letmein"
tar -czf /tmp/backup.tgz /var/data
EOF

RUN cat > /home/user/scripts/deploy.sh <<'EOF'
#!/bin/bash
# Deployment helper
export DB_password="P@ssw0rd!"
echo "Deployment complete"
EOF

RUN cat > /home/user/scripts/clean.sh <<'EOF'
#!/bin/bash
# Cleanup utility
# (no secrets here)
EOF

RUN chmod 755 /home/user/scripts/*.sh && \
    chmod -R a+rX /home/user && \
    chmod a+w /home/user /home/user/scripts

LABEL Author="your_name_here"