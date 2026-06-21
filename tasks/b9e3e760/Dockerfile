FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create a non-root user for the exercise
RUN useradd -m -s /bin/bash user

# Prepare the initial mock DNS data (read-only file, 0644)
RUN mkdir -p /home/user/mock_dns

RUN cat <<'EOF' > /home/user/mock_dns/hosts_mapping
backup1.example.com 192.168.10.11
backup2.example.com 192.168.10.12
db1.internal.local 10.0.0.21
db2.internal.local 10.0.0.22
EOF

RUN chmod 0644 /home/user/mock_dns/hosts_mapping

# Ensure the container's non-root user (and any caller) can work
RUN chown -R user:user /home/user && \
    chmod 0777 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8