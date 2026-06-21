FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare workspace
RUN mkdir -p /home/user/capacity_planner/input

# Create sample CSV
RUN cat <<'EOF' > /home/user/capacity_planner/input/usage_samples.csv
timestamp,cpu_percent,mem_used_mb,disk_used_gb,net_in_kbps,net_out_kbps
2023-01-01 00:00,45.6,2300,120,300,250
2023-01-01 01:00,55.2,2400,121,350,270
2023-01-01 02:00,65.4,2500,123,400,310
2023-01-01 03:00,35.8,2200,119,280,200
EOF

# Set permissions
RUN chmod 0644 /home/user/capacity_planner/input/usage_samples.csv
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/capacity_planner && \
    chmod 0777 /home/user/capacity_planner/input

# Help text (from %help)
# Container for capacity-planner task.

CMD ["sh", "-c", "echo \"Container for capacity-planner task. Open a shell to begin.\""]