FROM ubuntu:22.04

LABEL Author="db-reliability-task"
LABEL Description="Base image for dotenv + env capture exercise"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/db_backup && \
    chmod -R 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user

CMD ["echo", "Container for the dotenv + env capture exercise."]