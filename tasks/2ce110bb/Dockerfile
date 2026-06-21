# Based on localimage bootstrap: using Ubuntu 22.04 as base
FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    mkdir -p /home/user/iot_config

RUN cat > /home/user/iot_config/device_config.json <<'JSON'
[
  {"id":"dev-001", "status":"active", "ip":"192.168.1.10"},
  {"id":"dev-002", "status":"pending"},
  {"id":"dev-003", "status":"active", "ip":"192.168.1.12"},
  {"id":"dev-004", "status":"inactive", "ip":"192.168.1.13"},
  {"id":"dev-005", "status":"pending"}
]
JSON

RUN cat > /home/user/iot_config/device_schema.json <<'JSON'
{"required": ["id", "status", "ip"]}
JSON

RUN chown -R user:user /home/user && \
    chmod 700 /home/user/iot_config && \
    chmod 600 /home/user/iot_config/device_config.json && \
    chmod 600 /home/user/iot_config/device_schema.json && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment section
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN chmod 755 /home/user

# Runscript equivalent
CMD ["bash", "-c", "echo 'Container for IoT validation task. Launch an interactive shell or execute commands directly.'"]