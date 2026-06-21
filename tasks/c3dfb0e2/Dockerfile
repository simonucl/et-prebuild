FROM ubuntu:22.04

# Update apt repository and install Python + pip
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the capacity-planning task
# Create the home directory structure that the agent will use.
RUN mkdir -p /home/user/raw_stats && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/raw_stats

# containerA.txt
RUN cat > /home/user/raw_stats/containerA.txt <<'EOF'
CPU: 17.5
Memory_Used_MB: 256
Memory_Limit_MB: 1024
Network_In_KB: 10240
Network_Out_KB: 20480
EOF

# containerB.txt
RUN cat > /home/user/raw_stats/containerB.txt <<'EOF'
CPU: 17.5
Memory_Used_MB: 256
Memory_Limit_MB: 1024
Network_In_KB: 10240
Network_Out_KB: 20480
EOF

RUN cat > /home/user/raw_stats/containerB.txt <<'EOF'
CPU: 42.3
Memory_Used_MB: 512
Memory_Limit_MB: 2048
Network_In_KB: 5120
Network_Out_KB: 10240
EOF

RUN chmod 0644 /home/user/raw_stats/containerA.txt /home/user/raw_stats/containerB.txt && \
    chmod 755 /home/user

# Labels
LABEL Author="cap-planning-task"

# Default command
CMD echo "This container sets up the environment for the capacity-planning exercise." && \
    echo "To begin, open a shell inside the container and follow the task instructions."