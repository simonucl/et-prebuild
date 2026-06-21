FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-venv && \
    pip3 install --no-cache-dir pytest

# Create initial project directory structure
RUN mkdir -p /home/user/backup-tool && \
    mkdir -p /home/user/backup-archives/2023-06-01

# 1. version.txt (semantic version 2.5.0)
RUN printf '2.5.0\n' > /home/user/backup-tool/version.txt

# 2. CHANGELOG.md (initial content exactly as specified, ending with newline)
RUN cat > /home/user/backup-tool/CHANGELOG.md <<'EOF'
## [2.5.0] - 2023-05-20
- Added remote snapshot capability.

## [2.4.0] - 2023-04-10
- Introduced incremental compression.

EOF

# 3. Backup files
RUN printf 'Alpha backup file\n' > /home/user/backup-archives/2023-06-01/backup1.txt && \
    printf 'Beta backup file\n' > /home/user/backup-archives/2023-06-01/backup2.txt

# 4. Manifest with intentionally incorrect SHA-256 sums
RUN cat > /home/user/backup-archives/2023-06-01/manifest.sha256 <<'EOF'
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee  backup1.txt
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff  backup2.txt
EOF

# Make sure the student (non-root runtime user) can freely modify the project
RUN chmod -R a+rwX /home/user

# Clean up APT caches to keep image size small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin"

# Create a script to set up the environment at runtime
RUN echo '#!/bin/bash\nchmod 755 /home/user\nif [ -z "$(command -v python)" ] && [ -n "$(command -v python3)" ]; then\n    ln -sf /usr/bin/python3 /usr/bin/python 2>/dev/null || true\nfi\nexec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Create python symlink if it doesn't exist
RUN ln -sf /usr/bin/python3 /usr/bin/python 2>/dev/null || true

WORKDIR /home/user

# Help information (as comment):
# This container sets up the initial filesystem state for the
# "backup integrity" exercise. It pre-installs pytest and creates all
# prerequisite files and directories under /home/user without yet
# performing any of the actions the student must carry out (verification
# log, version bump, CHANGELOG update).