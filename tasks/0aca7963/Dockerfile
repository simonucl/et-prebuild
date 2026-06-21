FROM ubuntu:22.04

# Install Python3, pip, pytest, and required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user “user” (UID 1000) with home directory
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Prepare initial project tree and source data file
RUN mkdir -p /home/user/projects/flowdata

RUN cat <<'EOF' > /home/user/projects/flowdata/flows.log
2023-05-01T10:00:01Z	192.168.1.10	TCP	10.0.0.5	443	1024
2023-05-01T10:00:02Z	192.168.1.11	UDP	10.0.0.6	53	512
2023-05-01T10:00:03Z	192.168.1.12	TCP	10.0.0.7	22	2048
2023-05-01T10:00:04Z	192.168.1.13	UDP	10.0.0.8	161	256
EOF

# Permissions
RUN chown -R 1000:1000 /home/user/projects && \
    chmod 0755 /home/user/projects/flowdata && \
    chmod 0644 /home/user/projects/flowdata/flows.log

# Environment section
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default runscript
CMD ["/bin/bash"]