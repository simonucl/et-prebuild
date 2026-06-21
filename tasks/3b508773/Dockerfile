FROM ubuntu:22.04

# Author rotation-task-setup
# Description "Environment for credential-rotation one-liner exercise"
# This image provides the initial conditions for the credential-rotation
# exercise. The legacy credentials file is present at
# /home/user/container_secrets.env, and pytest is available for test execution.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    printf 'DB_USER=legacy\nDB_PASS=OldP@ssword123\n' > /home/user/container_secrets.env && \
    chmod 666 /home/user/container_secrets.env && \
    rm -f /home/user/rotation.log && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:$PATH

CMD echo "This container is prepared for the credential-rotation task." && \
    echo "Run your one-liner in an interactive shell or via 'docker run'."