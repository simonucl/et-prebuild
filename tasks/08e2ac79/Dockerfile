FROM ubuntu:22.04

# Install required tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        jq \
        python3-pip \
        ca-certificates \
        --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Python packages for testing inside the container
RUN pip3 install --no-cache-dir pytest jsonschema

# Create directory structure
RUN mkdir -p /home/user/projects/profile/schema

# run1.json
RUN cat >/home/user/projects/profile/run1.json <<'EOF'
[
  {
    "process": "nginx",
    "cpu_usage": 12.5,
    "mem_usage": 150.2,
    "threads": 4,
    "pid": 1023
  },
  {
    "process": "redis",
    "cpu_usage": 7.9,
    "mem_usage": 85.0,
    "threads": 2,
    "pid": 1078
  }
]
EOF

# run2.json
RUN cat >/home/user/projects/profile/run2.json <<'EOF'
[
  {
    "process": "postgres",
    "cpu_usage": 18.2,
    "mem_usage": 230.4,
    "threads": 5,
    "pid": 1337
  }
]
EOF

# Draft-07 schema file
RUN cat >/home/user/projects/profile/schema/usage_summary.schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Usage Summary",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["process", "cpu_usage", "mem_usage"],
    "additionalProperties": false,
    "properties": {
      "process": { "type": "string" },
      "cpu_usage": { "type": "number", "minimum": 0 },
      "mem_usage": { "type": "number", "minimum": 0 }
    }
  }
}
EOF

# Permissions
RUN chmod -R 777 /home/user/projects/profile

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user