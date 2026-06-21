# Converted from Apptainer .def
FROM ubuntu:22.04

# Install Python tooling including pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/releases/release_2023-09-01 && \
    mkdir -p /home/user/releases/release_2023-09-08 && \
    mkdir -p /home/user/deployments

# Seed build.info for 2023-09-01
RUN cat <<'EOF' > /home/user/releases/release_2023-09-01/build.info
BUILD_ID: 202309011230
VERSION: v1.4.2
COMMIT: 1a2b3c4d
EOF

# Seed build.info for 2023-09-08
RUN cat <<'EOF' > /home/user/releases/release_2023-09-08/build.info
BUILD_ID: 202309081305
VERSION: v1.5.0
COMMIT: 5d6e7f8g
EOF

# Seed deployment_status.log
RUN cat <<'EOF' > /home/user/deployments/deployment_status.log
[2023-09-01 12:30] release_2023-09-01: SUCCESS
[2023-09-01 12:45] release_2023-09-01: DEPLOYED
[2023-09-08 13:15] release_2023-09-08: FAILED
[2023-09-08 13:40] release_2023-09-08: ROLLBACK_COMPLETED
EOF

# Permissions
RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user/releases /home/user/deployments && \
    chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8