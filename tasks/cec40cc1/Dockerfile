FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer task setup"
LABEL Description="Environment with starter biomedical CSV data and pytest installed."

# Non-interactive apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test-runner
RUN pip3 install --no-cache-dir pytest

# Create user and data directory
RUN useradd -m -s /bin/bash user && \
    mkdir -p /home/user/data

# Populate starter dataset
RUN cat << 'EOF' > /home/user/data/raw_measurements.csv
subject_id,temperature,heart_rate
S1,36.6,72
S2,37.1,75
S3,36.9,70
S4,37.3,80
S5,36.8,68
EOF

# Permissions: directory 755, files 644
RUN chmod 755 /home/user/data && \
    chmod 644 /home/user/data/raw_measurements.csv && \
    chown -R user:user /home/user

# Set working directory
WORKDIR /home/user

# Set default user
USER user