FROM ubuntu:22.04

# Install Python and pytest for the validation suite
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/project/data

# Create the CSV file
RUN cat >/home/user/project/data/users.csv <<'EOF'
id,first_name,last_name,email
1,Jane,Doe,jane.doe@example.com
2,John,Smith,john.smith@example.com
3,Alice,Brown,alice.brown@example.com
EOF

# Set safe permissions: readable by anyone, writable by owner
RUN chmod 0644 /home/user/project/data/users.csv && \
    chmod 0755 /home/user /home/user/project /home/user/project/data

# Labels
LABEL Maintainer="Container prep for CSV → JSON exercise"
LABEL Description="Initial environment with users.csv and pytest installed."