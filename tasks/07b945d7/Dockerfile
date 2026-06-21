FROM ubuntu:22.04

# Help:
# This container provides the starting file-system layout for the
# "deploy version 1.2.3" exercise. It already contains:
#   • /home/user/app/releases/1.2.2/app.jar
#   • /home/user/app/current → /home/user/app/releases/1.2.2
# Students are expected to create the 1.2.3 release, update the symlink,
# and write the deployment log as described in the assignment. Pytest is
# pre-installed so that the autograder can validate their work.

LABEL Author="TaskSetup"
LABEL Purpose="Initial state for deployment-automation exercise (version 1.2.3 prep)"

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    mkdir -p /home/user/app/releases/1.2.2 && \
    echo 'dummy bytecode for version 1.2.2' > /home/user/app/releases/1.2.2/app.jar && \
    chmod 644 /home/user/app/releases/1.2.2/app.jar && \
    ln -sf /home/user/app/releases/1.2.2 /home/user/app/current

RUN chmod -R a+rwX /home/user
RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1