# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python 3 and pytest for the grading harness
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare the initial lab state in /home/user/hardening_test
# ------------------------------------------------------------------
RUN mkdir -p /home/user/hardening_test

# 1. sshd_config (7 lines)
RUN cat > /home/user/hardening_test/sshd_config <<'EOF'
# Sample OpenSSH daemon configuration for the lab
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
# End of file
EOF

# 2. sysctl.conf (4 lines)
RUN cat > /home/user/hardening_test/sysctl.conf <<'EOF'
# Kernel sysctl configuration
vm.swappiness = 10
fs.file-max = 65535
# End of file
EOF

# 3. login.defs (5 lines - pay attention to exact spacing)
RUN cat > /home/user/hardening_test/login.defs <<'EOF'
# Shadow password suite configuration
UID_MIN                  1000
UID_MAX                 60000
UMASK                    077
# End of file
EOF

# Permissions
RUN chmod 755 /home/user/hardening_test && \
    chmod 644 /home/user/hardening_test/*

# Keep the regular PATH so python/pytest are found
ENV PATH="$PATH"