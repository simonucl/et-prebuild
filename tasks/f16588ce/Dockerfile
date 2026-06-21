# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help text from %help
# This container image sets up the initial state for an SSH key-rotation
# exercise. It pre-installs Python, pytest, and OpenSSH client utilities,
# creates /home/user/.ssh with the required authorized_keys content, and
# leaves the rest of the task for the learner to complete.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/.ssh && \
    chmod 700 /home/user/.ssh

RUN cat <<'EOF' > /home/user/.ssh/authorized_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDSgcf5xgxN0R8vG5YkNVrYJv1nVbWcv1O3MH8b6XAQ1 old-key-2023
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4an1j2xy7b3Dx3XcX8GpXxFfXriYrAYx0QHoQOH9d6QhvzXnYFho7ozatajIuHQw6mbeid8X8oI6INBnNw+9xCLdfDUbqMf95xTeNwCvufqJgHE4vvAJ8NjgrZpTr6lYQkPzwHC27bMqf+AKeFEg3UhYg2uscd/lXFk4Isllwz6TQ1iXwRXy2U1UXoCM deployment-key
EOF

RUN chmod 600 /home/user/.ssh/authorized_keys && \
    chown -R root:root /home/user && \
    chmod 755 /home/user

# Labels
LABEL Author="ssh-key-rotation-setup"