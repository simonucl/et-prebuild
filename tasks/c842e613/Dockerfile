# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/raw_profiles && \
    chmod 0755 /home/user/raw_profiles

RUN cat << 'EOF' > /home/user/raw_profiles/app_service.profile
# Profile data for app_service
# timestamp cpu_percent mem_mb
2024-06-20T12:00:00Z 35.5 1530
2024-06-20T12:00:05Z 42.0 1548
2024-06-20T12:00:10Z 27.3 1522
2024-06-20T12:00:15Z 55.1 1555
2024-06-20T12:00:20Z 48.6 1540
2024-06-20T12:00:25Z 31.2 1528
EOF

RUN chmod 0644 /home/user/raw_profiles/app_service.profile

LABEL Author="Apptainer Task Setup"
LABEL Description="Environment prepared for the performance-engineer trace transformation task."

ENV PATH="/usr/bin:/usr/local/bin:$PATH"

CMD ["/bin/bash"]