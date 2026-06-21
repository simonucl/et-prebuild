# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading tests
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create the required initial directory structure and seed data file
# ------------------------------------------------------------------
RUN mkdir -p /home/user/environments

# Create the source TSV file with the exact required contents
RUN cat > /home/user/environments/test_servers.tsv <<'EOF'
web-01	10.10.1.11	8080	Alice
api-01	10.10.1.21	9000	Bob
db-01	10.10.1.31	5432	Charlie
cache-01	10.10.1.41	6379	David
mq-01	10.10.1.51	5672	Eve
EOF

# Ensure the student (non-root) user can write inside the environment directory
RUN chmod -R 777 /home/user/environments && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Container for TSV column-extraction task.
# Run your shell commands inside /home/user/environments to complete the exercise.