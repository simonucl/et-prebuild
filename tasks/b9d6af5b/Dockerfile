FROM ubuntu:22.04

# Labels
LABEL Author="configuration-manager-initializer"
LABEL Description="Environment for configuration-tracking assignment (mock API pre-populated, pytest installed)."

# Basic tooling and Python installation
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        curl \
        diffutils

# Install pytest for the grader/test-harness
RUN pip3 install --no-cache-dir pytest

# Create a non-root user
RUN useradd --create-home --shell /bin/bash user || true

# Pre-populate the mock API directory with the exact JSON resources
RUN MOCK_DIR=/home/user/mock_api && \
    mkdir -p "${MOCK_DIR}" && \
    printf '{"version":"1.0","settings":{"feature":false}}' > "${MOCK_DIR}/before.json" && \
    printf '{"version":"2.0","settings":{"feature":true}}' > "${MOCK_DIR}/after.json" && \
    chmod 755 /home/user && \
    chmod 755 "${MOCK_DIR}" && \
    chmod 644 "${MOCK_DIR}/before.json" "${MOCK_DIR}/after.json"

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "echo 'This container sets up the initial environment for the configuration-tracking assignment.' && echo 'Invoke your own commands with: docker exec <container> <command>' && echo 'Example: docker run -it <image> bash'"]