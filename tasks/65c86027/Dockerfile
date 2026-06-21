# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install required software
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create home and project structure
RUN mkdir -p /home/user/app

# Create template environment file
RUN cat > /home/user/app/sample.env <<'EOF'
# Sample configuration file
APP_ENV=development
RELEASE_TAG=dev
EOF

# Ensure non-root users can work within the project directory
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

# Metadata from Apptainer labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container pre-populated for release-manager task with pytest installed."

# Help text from Apptainer %help
# This container provides the starting filesystem state for the release-manager
# exercise. The student will create /home/user/app/.env and
# /home/user/deploy_summary.log during assessment. Pytest is installed for
# automated grading.