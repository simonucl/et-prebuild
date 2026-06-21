# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="security-eng"
LABEL Description="Apptainer image providing the initial state for the credentials-rotation task."

# ------------------------------------------------------------------
# Install Python tooling needed for the test harness
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the credential-rotation task
# ------------------------------------------------------------------

# Create the project directory structure
RUN mkdir -p /home/user/projects/secure-app

# Populate the original .env file with the legacy credentials
RUN cat > /home/user/projects/secure-app/.env <<'EOF'
OLD_API_KEY=oldkey123
OLD_SECRET=oldsecret321
EOF

# Make sure the entire /home/user tree is writable
RUN chmod -R 0777 /home/user

# Clean up apt caches to keep the image small
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Environment configuration (from %environment)
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Ensure expected permissions at runtime
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Help (from %help)
# ------------------------------------------------------------------
# This image provides the initial filesystem and tooling required
# for the credentials-rotation task.