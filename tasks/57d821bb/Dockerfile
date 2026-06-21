# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest for the test-suite
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state for the “RPM pending updates” task
# ------------------------------------------------------------------
# 1. Ensure the expected directory hierarchy exists
RUN mkdir -p /home/user/deployment/pending_updates

# 2. Create the three required RPM placeholder files
RUN set -e && \
    cd /home/user/deployment/pending_updates && \
    touch app-core-2.0.1.rpm \
          db-driver-5.3.0.rpm \
          ui-frontend-1.4.8.rpm && \
    chmod 644 *.rpm

# 3. Create an unprivileged 'user' account whose home is /home/user
RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user user; \
    fi

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Container help / run message
# ------------------------------------------------------------------
# Container for the RPM pending updates task.
# Use 'docker run -it <image> /bin/bash' to enter.
CMD echo "Container for the RPM pending updates task. Use 'docker run -it <image> /bin/bash' to enter."