FROM ubuntu:22.04

# Labels
LABEL Author="backup-sim exercise builder"
LABEL Description="Container for backup-metadata validation exercise"

# Basic OS packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates \
        curl \
        git \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python tooling – pytest is required by the automatic grader
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest jsonschema

# Create the initial directory tree and seed data
RUN mkdir -p /home/user/backup_sim/backups && \
    mkdir -p /home/user/backup_sim/schema

# JSON Schema
RUN cat > /home/user/backup_sim/schema/backup_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Backup Record",
  "type": "object",
  "required": ["backupDate", "hostname", "files"],
  "properties": {
    "backupDate": {
      "type": "string",
      "format": "date-time"
    },
    "hostname": {
      "type": "string"
    },
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "sha256"],
        "properties": {
          "path":   { "type": "string" },
          "sha256": { "type": "string", "pattern": "^[a-fA-F0-9]{32}$" }
        }
      }
    }
  }
}
EOF

# Valid backup: 2023-11-01
RUN cat > /home/user/backup_sim/backups/backup_2023-11-01.json <<'EOF'
{
  "backupDate": "2023-11-01T02:13:45Z",
  "hostname": "webserver1",
  "files": [
    {
      "path": "/etc/nginx/nginx.conf",
      "sha256": "b1946ac92492d2347c6235b4d2611184"
    },
    {
      "path": "/var/www/index.html",
      "sha256": "7d793037a0760186574b0282f2f435e7"
    }
  ]
}
EOF

# Intentionally INVALID JSON (contains a C-style comment)
RUN cat > /home/user/backup_sim/backups/backup_2023-12-06.json <<'EOF'
{
  "backupDate": "2023-12-06T04:05:22Z",
  "hostname": "db01",
  "files": [
    {
      "path": "/var/lib/mysql/ibdata1"
      /* missing sha256 field makes the document violate the schema */
    }
  ]
}
EOF

# Valid backup: 2023-12-20
RUN cat > /home/user/backup_sim/backups/backup_2023-12-20.json <<'EOF'
{
  "backupDate": "2023-12-20T00:00:01Z",
  "hostname": "fileserver",
  "files": [
    {
      "path": "/srv/files/document.pdf",
      "sha256": "9ae0ea9e3c9c6e1b9b6252c8395efdc1"
    },
    {
      "path": "/srv/files/report.doc",
      "sha256": "3c59dc048e8850243be8079a5c74d079"
    }
  ]
}
EOF

# Permissions – allow unprivileged container users to create validation/
RUN chmod -R a+rX /home/user && \
    chmod -R a+rwX /home/user/backup_sim

# Environment variables
ENV PATH=$PATH:/home/user/.local/bin

# Set working directory
WORKDIR /home/user

# Default command
CMD ["sh", "-c", "echo 'Backup-metadata validation exercise container.' && echo 'Enter the container and complete the tasks as instructed.'"]