FROM ubuntu:22.04

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get -y install --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the exercise
RUN mkdir -p /home/user/backup

# Create the full_backup.log with the exact required content
RUN cat > /home/user/backup/full_backup.log <<'EOF'
2024-06-01|00:15|37GB|OK
2024-06-02|00:17|40GB|OK
2024-06-03|00:20|38GB|FAIL
EOF

# Set permissions
RUN chmod 0644 /home/user/backup/full_backup.log && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/backup

CMD ["bash"]