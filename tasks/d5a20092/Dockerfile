FROM ubuntu:22.04

# Labels
LABEL Author="Capacity-Planning-Exercise"
LABEL Description="Environment prepared for January 2023 capacity report automation task."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create the non-privileged user expected by the exercise
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 user; \
    fi

# Base directory structure for the capacity-planning task
RUN mkdir -p /home/user/capacity/raw && \
    mkdir -p /home/user/capacity/reports

# Pre-populate the first January-2023 raw log file
RUN cat > /home/user/capacity/raw/server1_202301.log <<'EOF'
CPU_USED=42
MEM_USED=76
DISK_USED=63
EOF

# Pre-populate the second January-2023 raw log file
RUN cat > /home/user/capacity/raw/server2_202301.log <<'EOF'
CPU_USED=58
MEM_USED=68
DISK_USED=57
EOF

# Ownership and permissions (directories 755, files 644, owned by user:user)
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/capacity && \
    chmod 755 /home/user/capacity/raw && \
    chmod 755 /home/user/capacity/reports && \
    chmod 644 /home/user/capacity/raw/*.log

WORKDIR /home/user

# Default command
CMD ["echo", "Container for the January-2023 capacity-planning exercise. Invoke your own commands as needed."]