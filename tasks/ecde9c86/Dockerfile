FROM ubuntu:22.04

# Help / runscript content
# Container ready for the capacity-planner assignment.
# Run the test suite with: pytest -q

LABEL org.opencontainers.image.title="Capacity Planner Assignment Base Image"
LABEL org.opencontainers.image.authors="ChatGPT Automation"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        make && \
    pip3 install --no-cache-dir pytest

# Create input directory and file
RUN mkdir -p /home/user/data && \
    cat <<'EOF' > /home/user/data/usage.tsv
timestamp	cpu_percent	mem_percent	disk_percent
2023-01-01T00:00:00Z	15	40	60
2023-01-01T01:00:00Z	25	55	65
2023-01-01T02:00:00Z	20	50	70
EOF

# Ensure work directory does not exist
RUN rm -rf /home/user/capacity_planner || true

# Set permissions
RUN chmod -R a+rwx /home/user && chmod 755 /home/user

# Clean apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

CMD echo "Container ready for the capacity-planner assignment." && echo "Run the test suite with:  pytest -q"