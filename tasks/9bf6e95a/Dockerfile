FROM ubuntu:22.04

# Author MobileCI Task Setup
# Description "Initial state for mobile_builder CID extraction task"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash -u 1000 user

RUN mkdir -p /home/user/.ci && \
    cat > /home/user/.ci/containers_running.txt << 'EOF'
CONTAINER ID   IMAGE                COMMAND               CREATED        STATUS          PORTS     NAMES
a1b2c3d4e5f6   mobile-app-builder   "/entrypoint.sh"      2 hours ago    Up 2 hours               mobile_builder
d7e8f9g0h1i2   test-runner          "/start.sh"           30 minutes ago Up 30 minutes            test_runner
EOF

RUN chown -R user:user /home/user && \
    chmod 755 /home/user

ENV PATH="/home/user/.local/bin:$PATH"

CMD echo "Container for mobile_builder CID extraction task." && echo "Switch to the 'user' account to begin:  su - user"