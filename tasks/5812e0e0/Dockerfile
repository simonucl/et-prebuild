FROM ubuntu:22.04

# Labels
LABEL Author="release-manager-setup"
LABEL Description="Container image prepared for the 'release-manager' task with initial release data and pytest installed."

# Ensure basic tools are present
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create initial directory tree
RUN mkdir -p /home/user/releases/v2.0.0 \
    /home/user/releases/v2.1.0 \
    /home/user/releases/v3.0.0-beta

# v2.0.0 CHANGELOG.txt
RUN cat > /home/user/releases/v2.0.0/CHANGELOG.txt <<'EOF'
v2.0.0 - 2023-05-10 Major release

* Added multi-tenant support
* Deprecated legacy API
EOF

# v2.0.0 RELEASE_NOTES.md
RUN cat > /home/user/releases/v2.0.0/RELEASE_NOTES.md <<'EOF'
# Release Notes for v2.0.0

## Highlights
- Full RBAC implementation
EOF

# v2.1.0 CHANGELOG.txt
RUN cat > /home/user/releases/v2.1.0/CHANGELOG.txt <<'EOF'
v2.1.0 - 2023-08-12 Minor release

* Improved logging
EOF

# v2.1.0 RELEASE_NOTES.md
RUN cat > /home/user/releases/v2.1.0/RELEASE_NOTES.md <<'EOF'
# Release Notes for v2.1.0

## Improvements
- Faster cache invalidation
EOF

# v3.0.0-beta CHANGELOG.txt
RUN cat > /home/user/releases/v3.0.0-beta/CHANGELOG.txt <<'EOF'
v3.0.0-beta - 2024-01-20 Beta release

* Brand-new micro-kernel
EOF

# v3.0.0-beta RELEASE_NOTES.md
RUN cat > /home/user/releases/v3.0.0-beta/RELEASE_NOTES.md <<'EOF'
# Release Notes for v3.0.0-beta

## Beta caveats
- May eat your data
EOF

# Set permissions: directories 755, files 644
RUN find /home/user/releases -type d -exec chmod 755 {} + && \
    find /home/user/releases -type f -exec chmod 644 {} + && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH