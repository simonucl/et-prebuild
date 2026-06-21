FROM ubuntu:22.04

# Labels
LABEL Author="hardener exercise container"
LABEL Description="Environment for version-bump task with pytest pre-installed."

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Base tooling
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial workspace for the exercise
RUN mkdir -p /home/user/hardener && \
    chmod 0777 /home/user /home/user/hardener || true

# 1. version.txt (semantic version with NO trailing newline)
RUN printf '1.4.2' > /home/user/hardener/version.txt && \
    chmod 0666 /home/user/hardener/version.txt

# 2. CHANGELOG.md (exact content specified in task)
RUN cat > /home/user/hardener/CHANGELOG.md <<'EOF'
## [1.4.2] - 2023-08-07
### Added
- Initial iptables hardening rules.

### Changed
- Tuned /proc sysctl defaults.

### Fixed
- Corrected typo in sshd_config example.
EOF

RUN chmod 0666 /home/user/hardener/CHANGELOG.md

# 3. Placeholder configuration samples - harden-ssh.conf
RUN cat > /home/user/hardener/harden-ssh.conf <<'EOF'
# Example SSH hardening configuration (content irrelevant for task)
Protocol 2
EOF

# harden-sysctl.conf
RUN cat > /home/user/hardener/harden-sysctl.conf <<'EOF'
# Example sysctl hardening configuration (content irrelevant for task)
net.ipv4.ip_forward = 0
EOF

RUN chmod 0666 /home/user/hardener/harden-ssh.conf /home/user/hardener/harden-sysctl.conf

# Ensure no previous bump log is present
RUN rm -f /home/user/hardener/bump.log || true

# Set permissions on home directory
RUN chmod 755 /home/user