FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT - Automatic build file"
LABEL Description="Environment pre-loaded with capacity-planner sample INI data and pytest."

# Install required system packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python testing framework
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/capacity_planner/data

# Create server01.ini
RUN cat > /home/user/capacity_planner/data/server01.ini <<'EOF'
[2024-08-01]
CPU=55
Memory=6820
Disk=120

[2024-08-02]
CPU=60
Memory=7000
Disk=118

[2024-08-03]
CPU=58
Memory=6950
Disk=117
EOF

# Create server02.ini
RUN cat > /home/user/capacity_planner/data/server02.ini <<'EOF'
[2024-08-01]
CPU=70
Memory=12000
Disk=250

[2024-08-02]
CPU=75
Memory=11850
Disk=249

[2024-08-03]
CPU=73
Memory=11900
Disk=248
EOF

# Create server03.ini
RUN cat > /home/user/capacity_planner/data/server03.ini <<'EOF'
[2024-08-01]
CPU=30
Memory=4000
Disk=80

[2024-08-02]
CPU=28
Memory=3950
Disk=79

[2024-08-03]
CPU=27
Memory=3900
Disk=78
EOF

# Ensure appropriate permissions
RUN chmod 755 /home /home/user /home/user/capacity_planner /home/user/capacity_planner/data || true && \
    chmod 644 /home/user/capacity_planner/data/*.ini

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user

CMD ["echo", "Container for capacity-planner task. Execute your scripts inside."]