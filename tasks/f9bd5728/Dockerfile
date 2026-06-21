FROM ubuntu:22.04

# Container for the “Log the SHA-256 signature of the retired credential file” task.
# It provides:
#   /home/user/secrets/old_credentials.txt (zero-byte placeholder file)
#   Python 3 + pytest (needed for automated grading)
# The student must create /home/user/rotation/credential_rotation.log according to the task requirements.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/secrets && \
    touch /home/user/secrets/old_credentials.txt && \
    truncate -s 0 /home/user/secrets/old_credentials.txt && \
    chmod 644 /home/user/secrets/old_credentials.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin