FROM ubuntu:22.04

# Help text
# Container for the “disk-usage audit” task.
# Includes:
#   - Python 3 + pytest for automated testing
#   - Pre-populated /home/user/data directory with required files
# The /home/user/audit directory is intentionally NOT created.

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data/subdir1 && \
    mkdir -p /home/user/data/subdir2 && \
    printf 'Hello compliance\n' > /home/user/data/fileA.txt && \
    printf 'Log entry 1\nLog entry 2\n' > /home/user/data/fileB.log && \
    dd if=/dev/zero bs=1024 count=1 of=/home/user/data/subdir1/fileC.bin status=none && \
    printf 'Nested compliance data\n' > /home/user/data/subdir2/nested.txt && \
    chmod 0755 /home/user && \
    find /home/user/data -type d -exec chmod 0755 {} + && \
    find /home/user/data -type f -exec chmod 0644 {} +

# Labels (from %labels)
LABEL Author="Auto-generated for disk-usage audit task"