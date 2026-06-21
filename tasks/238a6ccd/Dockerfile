FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare dataset in /home/user/data
RUN mkdir -p /home/user/data
RUN cat <<'EOF' > /home/user/data/shard_a.csv
user_id,timestamp,value
101,2023-01-01,0.5
102,2023-01-02,0.6
103,2023-01-03,0.7
104,2023-01-04,0.8
105,2023-01-05,0.9
106,2023-01-06,1.0
107,2023-01-07,1.1
EOF

RUN cat <<'EOF' > /home/user/data/shard_b.csv
user_id,timestamp,value
104,2023-01-04,0.8
105,2023-01-05,0.9
108,2023-01-08,1.2
109,2023-01-09,1.3
110,2023-01-10,1.4
101,2023-01-11,0.55
111,2023-01-12,1.5
EOF

# Create output directory and set permissions
RUN mkdir -p /home/user/output && \
    chmod -R 777 /home/user

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set directory permissions at runtime
RUN chmod 755 /home/user