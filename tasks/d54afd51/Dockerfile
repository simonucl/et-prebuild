FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the directory structure
RUN mkdir -p /home/user/run && \
    mkdir -p /home/user/optimization

# Provide the reference input file
RUN cat > /home/user/run/docker_stats_sample.log <<'EOF'
CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT     MEM %     NET I/O           BLOCK I/O         PIDS
bf27be1234ab   pg_db             72.10%    256MiB / 2GiB          12.5%     1.2GB / 980MB     40MB / 15MB       35
66beccaa9a22   redis_cache       1.23%     20MiB / 2GiB           0.9%      120MB / 80MB      5MB / 4MB         6
a9c8f312654b   nginx_web         0.05%     10MiB / 2GiB           0.5%      500MB / 300MB     1MB / 1MB         3
EOF

# Ensure readable permissions
RUN chmod 644 /home/user/run/docker_stats_sample.log && \
    chmod 755 /home/user/run && \
    chmod 755 /home/user/optimization

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="Exercise Builder"
LABEL Description="Environment for SQL workload optimisation practice – provides docker_stats_sample.log and pytest."

WORKDIR /home/user