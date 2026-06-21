# Help
# This image provides a clean environment for the “DNS status log” exercise.
# Pytest is pre-installed, and a writable /home/user directory is available.
# Expected output artefacts (/home/user/alerts and its log file) are absent at build time.

FROM ubuntu:22.04

# Basic development tools and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create non-root user "user"
RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        USER_UID=1000; \
        if getent passwd 1000 >/dev/null 2>&1; then \
            useradd -m -s /bin/bash user; \
        else \
            useradd -m -u "${USER_UID}" -s /bin/bash user; \
        fi; \
    fi && \
    mkdir -p /home/user && \
    chmod 755 /home/user

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="Generated for DNS sanity-check task"
LABEL Description="Base container with pytest installed and clean initial state (no alerts directory)."

CMD ["/bin/bash"]