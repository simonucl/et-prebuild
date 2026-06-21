FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container for legacy build smoke-test exercise with pytest pre-installed."

# Update APT and install Python + pip
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state required by the assignment
RUN mkdir -p /home/user/legacy_build

# Create the legacy build script
RUN cat >/home/user/legacy_build/run_legacy_build.sh <<'EOF'
#!/usr/bin/env bash
echo "Starting legacy build pipeline..."
sleep 1
echo "Compiling module alpha..."
sleep 1
echo "Running unit tests..."
sleep 1
echo "All tests passed."
sleep 1
echo "BUILD SUCCESSFUL"
EOF

# Script must *not* be executable at the outset (0644)
RUN chmod 0644 /home/user/legacy_build/run_legacy_build.sh

# Ensure the student (host user UID/GID is usually 1000) owns the tree
# so they can chmod, mkdir, write logs, etc.
RUN chown -R 1000:1000 /home/user || true

# Reasonable directory permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/legacy_build

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"