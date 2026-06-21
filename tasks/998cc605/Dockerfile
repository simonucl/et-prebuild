FROM ubuntu:22.04

# Basic OS utilities and Python tooling
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip jq && \
    pip3 install --no-cache-dir pytest jsonschema && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial directory structure and JSON specification files
RUN mkdir -p /home/user/release && \
    chmod 0777 /home/user/release

# env_schema.json
RUN cat > /home/user/release/env_schema.json <<'EOF'
{"$schema":"http://json-schema.org/draft-07/schema#","type":"object","required":["version","services"],"properties":{"version":{"type":"string","pattern":"^[0-9]+\\.[0-9]+\\.[0-9]+$"},"services":{"type":"array","minItems":1,"items":{"type":"object","required":["name","image","ports"],"properties":{"name":{"type":"string"},"image":{"type":"string"},"ports":{"type":"array","minItems":1,"items":{"type":"integer","minimum":1,"maximum":65535}}},"additionalProperties":false}}},"additionalProperties":false}
EOF

# env_descriptor.json
RUN cat > /home/user/release/env_descriptor.json <<'EOF'
{"version":"1.4.0","services":[{"name":"auth-service","image":"registry.example.com/auth:1.4.0","ports":[8080]},{"name":"payments-service","image":"registry.example.com/payments:2.1.3","ports":[9000,9001]}]}
EOF

RUN chmod 0644 /home/user/release/env_schema.json /home/user/release/env_descriptor.json

# Environment settings
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user