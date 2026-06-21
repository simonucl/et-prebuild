FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create the capacity-planner directory tree and seed the log files
RUN mkdir -p /home/user/capacity_planner/logs

# ----- app1.log (112 bytes, 3 lines) -----
RUN cat > /home/user/capacity_planner/logs/app1.log <<'EOF'
2023-10-01 10:00:00 INFO App1 started
2023-10-01 10:05:00 WARN Low memory
2023-10-01 10:10:00 INFO App1 stopped
EOF

# ----- app2.log (45 bytes, 2 lines) -----
RUN cat > /home/user/capacity_planner/logs/app2.log <<'EOF'
ERROR Something bad happened
INFO Recovering
EOF

# ----- app3.log (16 bytes, 1 line) -----
RUN cat > /home/user/capacity_planner/logs/app3.log <<'EOF'
DEBUG Heartbeat
EOF

# ----- app4.log (117 bytes, 4 lines) -----
RUN cat > /home/user/capacity_planner/logs/app4.log <<'EOF'
INFO Service started successfully
WARN CPU usage detectd
WARN High Memory usage detected
ERROR OutOfMemory exception
EOF

# ----- app5.log (10 bytes, 5 lines) -----
RUN cat > /home/user/capacity_planner/logs/app5.log <<'EOF'
x
x
x
x
x
EOF

# Set the specific modification times required by the tests
RUN touch -d @1680000000 /home/user/capacity_planner/logs/app1.log && \
    touch -d @1680003600 /home/user/capacity_planner/logs/app2.log && \
    touch -d @1680007200 /home/user/capacity_planner/logs/app3.log && \
    touch -d @1680010800 /home/user/capacity_planner/logs/app4.log && \
    touch -d @1680014400 /home/user/capacity_planner/logs/app5.log

# Permissions: world-readable files; directory searchable
RUN chmod 644 /home/user/capacity_planner/logs/*.log && \
    chmod 755 /home/user/capacity_planner /home/user/capacity_planner/logs && \
    chmod 755 /home/user