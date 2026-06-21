FROM ubuntu:22.04

# Labels
LABEL Author="AI-Generated"
LABEL Description="Initial state for IoT data-cleaning assignment (pytest pre-loaded)"

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        csvkit \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader / student
RUN pip3 install --no-cache-dir pytest

# Create the required pristine input state
RUN mkdir -p /home/user/iot_data

# Create device_A.csv
RUN cat >/home/user/iot_data/device_A.csv <<'EOF'
timestamp,temperature,humidity
2023-07-01T00:00:00Z,25.4,60
2023-07-01T01:00:00Z,,61
2023-07-01T02:00:00Z,26.1,62
EOF

# Create device_B.csv
RUN cat >/home/user/iot_data/device_B.csv <<'EOF'
timestamp,temperature,humidity
2023-07-01T00:30:00Z,24.0,
2023-07-01T01:30:00Z,24.5,59
2023-07-01T02:30:00Z,25.0,60
EOF

# Create device_C.csv
RUN cat >/home/user/iot_data/device_C.csv <<'EOF'
timestamp,temperature,humidity
2023-07-01T00:15:00Z,23.9,58
2023-07-01T01:15:00Z,24.3,59
2023-07-01T02:15:00Z,,57
EOF

# Create device_registry.json
RUN cat >/home/user/device_registry.json <<'EOF'
[
  {"device_id":"device_A","location":"Building1","type":"sensor"},
  {"device_id":"device_B","location":"Building2","type":"sensor"},
  {"device_id":"device_C","location":"Building3","type":"sensor"},
  {"device_id":"device_D","location":"Building4","type":"sensor"}
]
EOF

# Ensure correct permissions for non-root users
RUN chmod -R a+rX /home/user

# Make sure the output directory does NOT exist (or is empty)
RUN rm -rf /home/user/iot_output || true

# Environment variables
ENV PATH="$PATH:/home/user/.local/bin"

# Set working directory
WORKDIR /home/user