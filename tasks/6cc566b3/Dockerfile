# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install needed packages (rsync for the task; pytest for testing)
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        rsync && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create prerequisite directory structure and files
# ------------------------------------------------------------------
RUN mkdir -p /home/user/app/logs && \
    mkdir -p /home/user/app/config && \
    printf 'Log Start\n' > /home/user/app/logs/app.log && \
    chmod 0644 /home/user/app/logs/app.log && \
    printf 'setting1=value1\nsetting2=value2\n' > /home/user/app/config/settings.conf && \
    chmod 0644 /home/user/app/config/settings.conf

# ------------------------------------------------------------------
# Prepare the “remote-drop” location
# ------------------------------------------------------------------
RUN mkdir -p /home/user/remote-drop && \
    chmod 0755 /home/user/remote-drop

# ------------------------------------------------------------------
# Ensure a non-root user exists and owns /home/user
# ------------------------------------------------------------------
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi && \
    chown -R 1000:1000 /home/user

# ------------------------------------------------------------------
# Runtime environment setup
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# ------------------------------------------------------------------
# Metadata
# ------------------------------------------------------------------
LABEL Author="diagnostic-setup" \
      Description="Initial state container for diagnostic snapshot exercise"

USER user
WORKDIR /home/user