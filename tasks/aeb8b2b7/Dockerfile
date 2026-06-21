# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %runscript
# This container is prepared for the observability CSV task.
# Enter the container and follow the assignment instructions.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    OBS_DIR="/home/user/observability" && \
    mkdir -p "${OBS_DIR}"

RUN OBS_DIR="/home/user/observability" && \
    cat > "${OBS_DIR}/metrics_cpu.log" <<'EOF'
timestamp|host|cpu_usage_percent|load_average|context_switches
2024-12-01T12:00:00Z|server-a|37.5|0.89|2312
2024-12-01T12:05:00Z|server-a|42.1|0.92|2478
2024-12-01T12:10:00Z|server-a|45.0|0.95|2560
2024-12-01T12:15:00Z|server-a|39.2|0.90|2401
2024-12-01T12:20:00Z|server-a|41.8|0.93|2505
EOF

RUN OBS_DIR="/home/user/observability" && \
    cat > "${OBS_DIR}/metrics_mem.log" <<'EOF'
timestamp|host|mem_used_mb|mem_free_mb|swap_used_mb
2024-12-01T12:00:00Z|server-a|5678|1024|256
2024-12-01T12:05:00Z|server-a|5690|1012|256
2024-12-01T12:10:00Z|server-a|5705|997|256
2024-12-01T12:15:00Z|server-a|5710|992|256
2024-12-01T12:20:00Z|server-a|5725|977|256
EOF

RUN chmod -R a+rwX /home/user && chmod 755 /home/user

CMD echo "This container is prepared for the observability CSV task." && \
    echo "Enter the container and follow the assignment instructions."