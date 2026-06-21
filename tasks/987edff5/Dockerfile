# From local image reference replaced with base image
FROM ubuntu:22.04

# %post commands
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/compliance

RUN cat >/home/user/compliance/failed_logins.tsv <<'EOF'
username	ip_address	timestamp	attempts
alice	10.0.0.5	2023-08-01T12:01:22Z	3
bob	10.0.0.6	2023-08-01T12:02:17Z	7
carol	10.0.0.7	2023-08-01T12:04:03Z	5
dave	10.0.0.8	2023-08-01T12:05:55Z	10
EOF

RUN chmod 0755 /home/user /home/user/compliance && \
    chmod 0644 /home/user/compliance/failed_logins.tsv

# %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# %help
# This container is set up for the 'account-lockout policy' exercise.

# %runscript
CMD echo "This container is set up for the 'account-lockout policy' exercise." && \
    echo "Invoke your shell or tooling as needed."