FROM ubuntu:22.04

# Labels from %labels
LABEL Author="devsecops-bot"
LABEL Description="Apptainer image for DevSecOps time & locale policy exercise. Contains Python 3 and pytest; ensures /home/user exists but required task files are absent."

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user || true && \
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Convert chmod from %environment into RUN
RUN chmod 755 /home/user

# Convert PATH export into ENV
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH