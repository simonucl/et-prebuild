FROM ubuntu:22.04

# Base OS packages and Python tooling
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare the filesystem expected by the assignment's pre-checks
# Create writable $HOME for the (non-root) runtime user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Baseline directory structure
RUN mkdir -p /home/user/baseline_configs/ssh && \
    mkdir -p /home/user/baseline_configs/sysctl && \
    chmod 0755 /home/user/baseline_configs && \
    chmod 0755 /home/user/baseline_configs/ssh && \
    chmod 0755 /home/user/baseline_configs/sysctl

# Create the SSH baseline configuration file
RUN cat > /home/user/baseline_configs/ssh/sshd_config_baseline <<'EOF'
# Baseline SSH config
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
EOF

# Create the sysctl baseline configuration file
RUN cat > /home/user/baseline_configs/sysctl/sysctl_baseline.conf <<'EOF'
# Baseline sysctl
net.ipv4.ip_forward = 0
net.ipv6.conf.all.disable_ipv6 = 1
vm.swappiness = 10
EOF

# Correct file permissions (0644)
RUN chmod 0644 /home/user/baseline_configs/ssh/sshd_config_baseline && \
    chmod 0644 /home/user/baseline_configs/sysctl/sysctl_baseline.conf

# Environment variables
ENV PATH=$PATH:/home/user/.local/bin

# Set working directory
WORKDIR /home/user

CMD ["echo", "Container ready – baseline security configuration files are in place."]