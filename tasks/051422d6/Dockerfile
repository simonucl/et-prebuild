FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/secure

RUN cat >/home/user/secure/api_keys.txt <<'EOF'
analytics:ABCD1234OLD
data-collector:XYZ7890OLD
monitoring:MON123OLD
EOF

RUN chmod 777 /home/user/secure && \
    chmod 666 /home/user/secure/api_keys.txt

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8