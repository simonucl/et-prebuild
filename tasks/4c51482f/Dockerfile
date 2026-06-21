FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest

# Prepare starter project structure
RUN mkdir -p /home/user/dev/config

# JSON-Schema
RUN cat > /home/user/dev/config/project.schema.json <<'EOF'
{"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "required": ["name", "version", "dependencies"], "properties": {"name": {"type": "string"}, "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"}, "dependencies": {"type": "object", "additionalProperties": {"type": "string"}}}, "additionalProperties": false}
EOF

# Manifest file
RUN cat > /home/user/dev/config/project.json <<'EOF'
{"name":"sample-poc","version":"0.1.3","dependencies":{"express":"4.18.2","lodash":"4.17.21"}}
EOF

# Permissions
RUN chmod -R a+rwx /home/user/dev

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:$PATH"