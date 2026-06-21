# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata (from %help and %labels)
# Container for the performance-engineering task.
# Author: Performance-Engineering-Setup
# Description: Provides raw profiling logs and pytest for grading.

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/perf/raw && \
    chmod 755 /home/user && \
    chmod 755 /home/user/perf && \
    chmod 755 /home/user/perf/raw

RUN cat <<'EOF' > /home/user/perf/raw/app1.log
[2023-02-10 15:12:01] FUNC=initSystem   CPU_MS=5  MEM_MB=30
[2023-02-10 15:12:05] FUNC=loadConfig   CPU_MS=8  MEM_MB=45
[2023-02-10 15:12:10] FUNC=parseData    CPU_MS=25 MEM_MB=550
[2023-02-10 15:12:12] FUNC=renderFrame  CPU_MS=40 MEM_MB=300
EOF

RUN cat <<'EOF' > /home/user/perf/raw/app2.log
[2023-02-10 15:12:02] FUNC=connectDB    CPU_MS=30 MEM_MB=400
[2023-02-10 15:12:08] FUNC=queryDB      CPU_MS=80 MEM_MB=650
[2023-02-10 15:12:13] FUNC=closeDB      CPU_MS=10 MEM_MB=120
EOF

RUN cat <<'EOF' > /home/user/perf/raw/app3.log
[2023-02-10 15:12:03] FUNC=authUser     CPU_MS=60 MEM_MB=200
[2023-02-10 15:12:07] FUNC=updateCache  CPU_MS=15 MEM_MB=100
[2023-02-10 15:12:09] FUNC=compressData CPU_MS=50 MEM_MB=700
[2023-02-10 15:12:11] FUNC=encryptData  CPU_MS=35 MEM_MB=480
EOF

RUN chmod 644 /home/user/perf/raw/app*.log

CMD echo "Container for the performance-engineering task." && echo "Navigate to /home/user and begin your work."