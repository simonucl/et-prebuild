# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# 1. Install required OS packages and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# 2. Create non-root user
RUN useradd -m -s /bin/bash user

# 3. Create directories
RUN mkdir -p /home/user/backups/latest && \
    mkdir -p /home/user/schema

# 3.1 manifest.json
RUN cat << 'EOF' > /home/user/backups/latest/manifest.json
{
  "backupId": "BK2023-10-05",
  "createdBy": "backupd v2.4.1",
  "restorePoints": [
    {
      "id": "rp1",
      "timestamp": "2023-10-05T01:15:00Z",
      "sizeBytes": 52428800,
      "checksum": "c1a1e3f4"
    },
    {
      "id": "rp2",
      "timestamp": "2023-10-05T03:30:00Z",
      "sizeBytes": 52428800,
      "checksum": "d2b2e4f5"
    },
    {
      "id": "rp3",
      "timestamp": "2023-10-05T06:45:00Z",
      "sizeBytes": 52428800,
      "checksum": "e3c3f5a6"
    }
  ]
}
EOF

# 3.2 restore-schema.json
RUN cat << 'EOF' > /home/user/schema/restore-schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["backupId", "restorePoints"],
  "properties": {
    "backupId": { "type": "string", "const": "BK2023-10-05" },
    "restorePoints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "timestamp", "sizeBytes", "checksum"],
        "properties": {
          "id":        { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" },
          "sizeBytes": { "type": "integer", "minimum": 0 },
          "checksum":  { "type": "string" }
        }
      },
      "minItems": 1
    }
  }
}
EOF

# 4. Set ownership
RUN chown -R user:user /home/user

# Environment section
ENV PATH="/home/user/.local/bin:${PATH}"
RUN chmod 755 /home/user

# Run as user with bash as default
CMD ["bash"]