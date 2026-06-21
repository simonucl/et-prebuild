FROM ubuntu:22.04

# Update package lists and install required utilities
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        passwd

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory layout
RUN mkdir -p /home/user/raw_data

# Populate raw CSV files
RUN cat > /home/user/raw_data/records_A.csv <<'EOF'
id,value
1,10
2,20
3,30
EOF

RUN cat > /home/user/raw_data/records_B.csv <<'EOF'
id,value
4,40
5,50
6,60
EOF

# Ensure permissions
RUN chmod -R a+rX /home/user

# Add non-privileged user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

# Environment setup
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin

LABEL Author="ChatGPT"
LABEL Description="Container image for the tabular-data optimization task (raw CSVs staged, pytest installed)"