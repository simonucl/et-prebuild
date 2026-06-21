# Converted from Apptainer definition file

FROM ubuntu:22.04

# Update apt metadata and install Python along with venv support
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest globally for the grading tests
RUN pip3 install --no-cache-dir pytest

# Create a writable workspace for the student
RUN mkdir -p /home/user && chmod 0777 /home/user

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Apply home directory permissions at container start
RUN chmod 755 /home/user