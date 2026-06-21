FROM ubuntu:22.04

# Labels
LABEL Author="container-builder"
LABEL Description="Apptainer image providing the initial state for the resource-utilisation reporting task."

# Environment variables
ENV LC_ALL=C
ENV LANG=C

# Install Python tooling and pytest
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure under /home/user
RUN mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/data && \
    chmod 755 /home/user/data && \
    mkdir -p /home/user/reports && \
    chmod 755 /home/user/reports

# Populate the snapshot file with the exact contents expected by the test-suite
RUN cat > /home/user/data/ps_snapshot.txt <<'EOF'
PID COMMAND %CPU %MEM
1 systemd 0.1 0.3
45 python3 12.5 5.1
102 nginx 23.8 1.2
150 mysqld 34.2 12.3
200 redis-server 3.2 0.8
215 java 18.7 10.4
300 node 7.9 1.1
350 sshd 0.0 0.1
400 postgres 8.4 6.5
450 dockerd 2.1 1.9
EOF

RUN chmod 644 /home/user/data/ps_snapshot.txt

# Default command
CMD ["echo", "Capacity-planning exercise container – nothing to run by default."]