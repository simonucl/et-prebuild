FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Ubuntu 22.04 image prepared for data-science task: contains draft raw JSON files, jq, and pytest."

# Create user and home directory
RUN useradd -m -s /bin/bash user

# Create the required raw data directory
RUN mkdir -p /home/user/raw_data

# Create raw1.json
RUN cat > /home/user/raw_data/raw1.json <<'EOF'
{"id": "sensor-A", "timestamp": "2023-09-01T12:00:00Z", "value": 42.7, "tags": ["lab","temperature"]}
EOF

# Create raw2.json
RUN cat > /home/user/raw_data/raw2.json <<'EOF'
{"id": 123, "timestamp": "2023-09-01T12:05:00Z", "value": "40.1", "tags": ["lab","temperature"]}
EOF

# Create raw3.json
RUN cat > /home/user/raw_data/raw3.json <<'EOF'
{"id": "sensor-B", "timestamp": "BADDATE", "value": 37.2, "tags": "humidity"}
EOF

# Ensure sensible permissions
RUN chmod -R 755 /home/user

# Install system utilities and Python testing framework
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip jq ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8