# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---- Install Python and pytest ------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---- Create user and prepare directory layout --------------------------------
RUN set -e && \
    useradd -m -d /home/user -s /bin/bash user && \
    mkdir -p /home/user/data

# ---- Prepare initial input data ------------------------------------------------
RUN cat > /home/user/data/uptime_checks.log <<'EOF'
2024-05-20T00:00:00Z web-1 UP
2024-05-20T00:05:00Z web-1 DOWN
2024-05-20T00:10:00Z web-1 UP
2024-05-20T00:15:00Z web-2 UP
2024-05-20T00:20:00Z web-2 UP
2024-05-20T00:25:00Z web-2 DOWN
2024-05-20T00:30:00Z db-1 UP
2024-05-20T00:35:00Z db-1 UP
2024-05-20T00:40:00Z db-1 UP
EOF

# ---- Ensure sensible permissions ----------------------------------------------
RUN set -e && \
    chmod 0644 /home/user/data/uptime_checks.log && \
    chmod 0755 /home/user /home/user/data

# ---- Environment variables ----------------------------------------------------
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# ---- Help ---------------------------------------------------------------------
# Container for the uptime reporting task.
# Run your solution script manually after entering the shell, e.g.:
#   docker run -it <image> /bin/bash

USER user
WORKDIR /home/user
CMD ["/bin/bash"]