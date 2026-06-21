# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# Container providing the initial state for the “edge-computing deployment”
# exercise. Includes Python3, pytest, sqlite3, and a prepared staging CSV at
# /home/user/edge_staging/devices.csv.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
        sudo && \
    pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

RUN mkdir -p /home/user/edge_staging

RUN cat <<'EOF' > /home/user/edge_staging/devices.csv
id,hw_rev,location
1,A1,rack-01
2,B2,rack-02
3,A1,rack-03
EOF

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked chown -R 1000:1000 /home/user && \
    chmod 0755 /home/user/edge_staging && \
    chmod 0644 /home/user/edge_staging/devices.csv && \
    if [ -d /home/user/edge_deploy ]; then rm -rf /home/user/edge_deploy; fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

CMD ["sudo", "-u", "user", "-E", "/bin/bash"]