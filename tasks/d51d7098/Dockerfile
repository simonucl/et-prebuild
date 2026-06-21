FROM ubuntu:22.04

# This container sets up the initial state for the APT credential-rotation
# exercise and includes pytest for automated grading.

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user (helpful when the container is executed)
RUN useradd -m -s /bin/bash user || true

# Base directories
RUN install -m 755 -d /home/user && \
    install -m 755 -d /home/user/.config && \
    install -m 755 -d /home/user/.config/privrepo && \
    install -m 755 -d /home/user/.config/apt && \
    install -m 755 -d /home/user/.config/apt/trusted.gpg.d && \
    install -m 755 -d /home/user/keys

# Old credential file
RUN cat > /home/user/.config/privrepo/creds.conf <<'EOF'
token=OLD-TOKEN-2023
EOF

# Old (still-valid) signing key
RUN cat > /home/user/.config/apt/trusted.gpg.d/privrepo_old.gpg <<'EOF'
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

old dummy key
-----END PGP PUBLIC KEY BLOCK-----
EOF

# New signing key that the student must install
RUN cat > /home/user/keys/new_privrepo.gpg <<'EOF'
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

new dummy key
-----END PGP PUBLIC KEY BLOCK-----
EOF

# Permissions (readable by the future, non-root student user)
RUN chmod 644 /home/user/.config/privrepo/creds.conf && \
    chmod 644 /home/user/.config/apt/trusted.gpg.d/privrepo_old.gpg && \
    chmod 644 /home/user/keys/new_privrepo.gpg && \
    chmod 755 /home/user

LABEL Author="Apptainer task setup"