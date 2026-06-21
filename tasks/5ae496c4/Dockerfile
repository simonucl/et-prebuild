# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Prepare application directory structure and seed data
# ------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/app/logs

# Create VERSION file with trailing newline
RUN printf '2.5.6\n' > /home/user/app/VERSION

# Seed logs/app.log with required contents
RUN cat > /home/user/app/logs/app.log <<'LOGEOF'
[2024-05-15 10:12:34] INFO: Service started
[2024-05-15 10:12:35] ERROR: Unable to connect to database
[2024-05-15 10:12:36] WARN: Retrying connection
[2024-05-15 10:12:37] ERROR: Connection timed out
[2024-05-15 10:12:40] INFO: Shutdown complete
LOGEOF

# Ensure files/directories are writable by the runtime (unprivileged) user
RUN chmod -R a+rwX /home/user/app

# ------------------------------------------------------------
# Runtime environment setup
# ------------------------------------------------------------
RUN mkdir -p /home/user && chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin"