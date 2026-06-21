# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Exercise Builder" \
      Description="Container image providing the initial state for the 'Failed Login IP extraction' task."

# Update APT and install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create non-root working user
RUN useradd -m -s /bin/bash user

# Prepare initial dataset directory and file
RUN mkdir -p /home/user/data

RUN cat > /home/user/data/server_access.log <<'EOF'
2023-12-02 08:15:43 INFO user1 192.168.1.10 SUCCESS LOGIN
2023-12-02 08:16:10 WARN user2 10.0.0.5 FAILED LOGIN
2023-12-02 09:00:01 WARN user5 172.16.0.3 FAILED LOGIN
2023-11-30 18:12:00 WARN user9 10.0.0.5 FAILED LOGIN
2023-12-15 12:22:17 WARN user6 192.168.1.10 FAILED LOGIN
2023-12-20 10:55:00 INFO user3 10.0.0.5 SUCCESS LOGIN
2023-12-20 11:00:14 WARN user2 10.0.0.5 FAILED LOGIN
2023-12-31 23:59:59 WARN user7 203.0.113.1 FAILED LOGIN
EOF

# Ensure ownership and permissions belong to the non-root user
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

# Default command (equivalent to Apptainer runscript)
CMD bash -c "echo 'Container for audit-log exercise. Execute your commands inside a shell:' && exec /bin/bash \"$@\""