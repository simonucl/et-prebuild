FROM ubuntu:22.04

# Labels
LABEL Author="Edge-Computing-Task-Setup"
LABEL Description="Docker image providing initial state and pytest for IoT log-filtering exercise"

# ------------------------------------------------------------------
# 1. Install Python tooling and pytest
# ------------------------------------------------------------------
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# 2. Create user with UID 1000
# ------------------------------------------------------------------
RUN useradd -m -u 1000 -s /bin/bash user

# ------------------------------------------------------------------
# 3. Create the required directory structure and files
# ------------------------------------------------------------------
RUN mkdir -p /home/user/iot_deploy/logs

RUN cat > /home/user/iot_deploy/logs/sensor.log <<'EOF'
2023-07-01T10:00:00Z INFO device123 TEMP=75.2 HUM=40
2023-07-01T10:05:00Z ERROR device123 TEMP=82.5 HUM=42
2023-07-01T10:10:00Z WARN device456 TEMP=60.1 HUM=50
2023-07-01T10:15:00Z ERROR device789 TEMP=90.0 HUM=35
2023-07-01T10:20:00Z INFO device123 TEMP=78.3 HUM=45
2023-07-01T10:25:00Z ERROR device456 TEMP=87.4 HUM=47
2023-07-01T10:30:00Z INFO device789 TEMP=72.0 HUM=38
EOF

# ------------------------------------------------------------------
# 4. Permissions: directory 755, file 644, owned by uid 1000
# ------------------------------------------------------------------
RUN chmod 755 /home/user/iot_deploy/logs && \
    chmod 644 /home/user/iot_deploy/logs/sensor.log && \
    chown -R 1000:1000 /home/user/iot_deploy && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user