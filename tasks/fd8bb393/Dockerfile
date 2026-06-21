# Based on Apptainer localimage bootstrap (converted to a standard Ubuntu base)
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container for SQL psqlrc configuration task with pytest installed."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    rm -f /home/user/.psqlrc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Run script equivalent
CMD ["/bin/bash"]