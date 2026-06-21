# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: security-audit-template
# Description: Base image with initial state for Security Audit exercise and pytest pre-installed.

# 1. Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Create directory hierarchy with correct permissions
RUN set -e && \
    mkdir -p /home/user/security_audit/input && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/security_audit && \
    chmod 0755 /home/user/security_audit/input

# 3. Populate users.csv
RUN cat > /home/user/security_audit/input/users.csv << 'EOF'
username,uid,gid,home,shell,access_level
root,0,0,/root,/bin/bash,admin
alice,1001,1001,/home/alice,/bin/bash,standard
bob,1002,1002,/home/bob,/usr/sbin/nologin,restricted
carol,1003,1001,/home/carol,/bin/zsh,standard
dave,999,999,/home/dave,/bin/bash,standard
eve,1004,1004,/home/eve,/bin/fish,standard
mallory,1200,1002,/home/mallory,/bin/bash,restricted
EOF

RUN chmod 0644 /home/user/security_audit/input/users.csv

# 4. Populate groups.json
RUN cat > /home/user/security_audit/input/groups.json << 'EOF'
[
  {
    "gid": 0,
    "group_name": "root",
    "allowed_shells": ["/bin/bash"]
  },
  {
    "gid": 1001,
    "group_name": "developers",
    "allowed_shells": ["/bin/bash", "/bin/zsh"]
  },
  {
    "gid": 1002,
    "group_name": "ops",
    "allowed_shells": ["/usr/sbin/nologin"]
  },
  {
    "gid": 1004,
    "group_name": "interns",
    "allowed_shells": ["/bin/bash"]
  }
]
EOF

RUN chmod 0644 /home/user/security_audit/input/groups.json

# Runtime environment settings
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Ensure home directory permissions at runtime
RUN chmod 0755 /home/user

# This container sets up the initial state for the Security Audit task.
# Invoke your own commands or open a shell (docker run -it <image> bash).

LABEL Author="security-audit-template" \
      Description="Base image with initial state for Security Audit exercise and pytest pre-installed."