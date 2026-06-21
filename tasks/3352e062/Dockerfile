FROM ubuntu:22.04

# Update apt and install required tools
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest and jsonschema
RUN pip3 install --no-cache-dir pytest jsonschema

# Create base directory structure
RUN mkdir -p /home/user/releases/schema && \
    mkdir -p /home/user/releases/incoming && \
    chmod 777 /home/user/releases

# Create JSON-Schema file
RUN cat > /home/user/releases/schema/service-schema.json <<'EOF'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Microservice build descriptor",
  "type": "object",
  "required": ["service", "version", "commit", "buildDate"],
  "properties": {
    "service": { "type": "string" },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "commit": { "type": "string", "minLength": 8, "maxLength": 40 },
    "buildDate": { "type": "string", "format": "date-time" },
    "notes": { "type": "string" }
  },
  "additionalProperties": false
}
EOF

# Create incoming build-descriptor files
RUN cat > /home/user/releases/incoming/service-auth.json <<'EOF'
{
  "service": "auth",
  "version": "2.3.4",
  "commit": "1a2b3c4d",
  "buildDate": "2023-08-22T10:15:00Z",
  "notes": "Added support for OAuth2."
}
EOF

RUN cat > /home/user/releases/incoming/service-payment.json <<'EOF'
{
  "service": "payment",
  "version": "1.19.0",
  "commit": "9d8c7b6a",
  "buildDate": "2023-08-24T14:22:00Z"
}
EOF

RUN cat > /home/user/releases/incoming/service-ui.json <<'EOF'
{
  "service": "ui",
  "version": "5.7.1",
  "buildDate": "2023-08-25T08:05:00Z",
  "notes": "UI improvements."
}
EOF

# Set permissions
RUN chmod 755 /home/user /home/user/releases/schema /home/user/releases/incoming && \
    chmod 644 /home/user/releases/schema/service-schema.json && \
    chmod 644 /home/user/releases/incoming/*.json