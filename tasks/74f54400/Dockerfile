# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the automated tests
RUN mkdir -p /home/user/profiling

RUN cat > /home/user/profiling/cpu_usage.perf <<'EOF'
# Profiling Report - CPU Usage
Timestamp: 2020-11-20T10:00:00Z
AvgCPU: 73.4%
EOF

RUN cat > /home/user/profiling/mem_usage.perf <<'EOF'
# Profiling Report - Memory Usage
Timestamp: 2020-11-20T10:00:00Z
AvgMem: 512MB
EOF

RUN cat > /home/user/profiling/io_usage.perf <<'EOF'
# Profiling Report - Disk I/O
Timestamp: 2020-11-20T10:00:00Z
AvgIO: 120MB/s
EOF

# Permissions for future non-root agent
RUN chmod 777 /home/user && \
    chmod 755 /home/user/profiling && \
    chmod 644 /home/user/profiling/*.perf

# Environment variables
ENV PYTHONIOENCODING=utf-8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Labels
LABEL Author="example" \
      Description="Container for profiling backup task – provides initial .perf files and pytest"