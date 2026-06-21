FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare writable home and .ssh directories
RUN mkdir -p /home/user/.ssh && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/.ssh

# Install predefined authorized key
RUN cat <<'EOF' > /home/user/.ssh/authorized_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB3j6Lm9vDGf/oldexamplekey== dev@old
EOF
RUN chmod 0666 /home/user/.ssh/authorized_keys

# Replicate runscript behavior
ENTRYPOINT ["/bin/bash", "-c", "chmod 755 /home/user; exec \"$@\"", "--"]