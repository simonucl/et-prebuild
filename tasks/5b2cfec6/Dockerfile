# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="deployment-task-initializer" \
      Description="Container image prepared for CSV deployment task (inventory & updates input only)."

# Update apt and install Python + pip, then pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory structure
RUN mkdir -p /home/user/release && \
    chmod 755 /home/user && \
    chmod 755 /home/user/release

# inventory.csv
RUN cat > /home/user/release/inventory.csv <<'EOF'
server_id,hostname,env,current_version
1,web-1,production,2.4.10
2,web-2,production,2.4.10
3,db-1,staging,12.1.0
4,cache-1,production,1.9.3
5,api-1,staging,3.2.1
EOF

# updates.csv
RUN cat > /home/user/release/updates.csv <<'EOF'
server_id,target_version,window
1,2.4.11,2024-06-20
2,2.4.11,2024-06-20
3,12.1.1,2024-06-21
4,1.9.4,2024-06-20
5,3.2.2,2024-06-21
EOF

# Ensure world-readable permissions so the unprivileged agent can access them
RUN chmod 644 /home/user/release/inventory.csv /home/user/release/updates.csv

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Help text from %help / %runscript
# This image provides the initial state for the deployment task.
# Inventory and update CSVs are located in /home/user/release.
# Activate a shell to begin working on the assignment.

CMD ["/bin/bash"]