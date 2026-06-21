FROM ubuntu:22.04

# Labels
LABEL Author="compliance-setup"
LABEL Description="Container image prepopulated with schema and audit JSON files for compliance task"

# Update package lists and install required utilities
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the automated test-runner
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/data/schema && \
    mkdir -p /home/user/data/audit && \
    mkdir -p /home/user/audit_results

# Write schema file
RUN cat > /home/user/data/schema/system_config.schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["hostname", "os_version", "patch_level", "encryption_enabled"],
  "properties": {
    "hostname":           { "type": "string"  },
    "os_version":         { "type": "string"  },
    "patch_level":        { "type": "integer" },
    "encryption_enabled": { "type": "boolean" }
  },
  "additionalProperties": true
}
EOF

# Write audit JSON file - system1.json
RUN cat > /home/user/data/audit/system1.json << 'EOF'
{
  "hostname": "webserver01",
  "os_version": "Ubuntu 20.04",
  "patch_level": 5,
  "encryption_enabled": true
}
EOF

# Write audit JSON file - system2.json
RUN cat > /home/user/data/audit/system2.json << 'EOF'
{
  "hostname": "dbserver02",
  "os_version": "CentOS 8"
}
EOF

# Write audit JSON file - system3.json
RUN cat > /home/user/data/audit/system3.json << 'EOF'
{
  "hostname": 12345,
  "os_version": "Debian 10",
  "patch_level": 7,
  "encryption_enabled": true
}
EOF

# Set permissions
RUN chmod 1777 /home/user && \
    chmod -R a+rwX /home/user/audit_results && \
    chmod -R a+r /home/user/data

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user