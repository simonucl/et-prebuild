FROM ubuntu:22.04

# Make package management non‑interactive and install tools
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user/group with UID/GID 1000
RUN if ! getent group 1000 >/dev/null; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 user; fi

# Create sample configs directory
RUN mkdir -p /home/user/sample_configs

# Create sshd_config via heredoc
RUN cat > /home/user/sample_configs/sshd_config <<'EOF'
# This is a sample sshd_config
Port 22
PermitRootLogin yes
#PermitRootLogin prohibit-password
PasswordAuthentication yes
#PasswordAuthentication no
Subsystem sftp /usr/lib/openssh/sftp-server
EOF

# Set permissions
RUN chmod 0644 /home/user/sample_configs/sshd_config && \
    chmod 0755 /home/user/sample_configs && \
    chown -R 1000:1000 /home/user

# From %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

LABEL Author="Container prepared for OpenSSH hardening exercise"