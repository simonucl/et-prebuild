FROM ubuntu:22.04

# Update package index and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential

# Install pytest for the grader
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create the default working directory expected by the grader and make it writable
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Clean up apt caches to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Labels
LABEL Author="Incident-Snapshot-Task"
LABEL Description="Container prepared for the \"30-second high-frequency snapshot\" exercise. Pytest installed; no incident_001 artifacts present."

WORKDIR /home/user

CMD ["echo", "Container for incident snapshot task. Use an interactive shell or execute your scripts as needed."]