# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help/labels
LABEL Author="ChatGPT OpenAI"

ENV HOME=/home/user
ENV PATH="/usr/local/bin:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest jsonschema

RUN mkdir -p /home/user/credentials && \
    chmod 0777 /home/user /home/user/credentials || true

RUN cat <<'CREDS' > /home/user/credentials/creds.json
{
  "user": "service_account",
  "access_key": "AKIAOLD123456789",
  "secret_key": "oldSecretKeyValue",
  "rotation_date": "2022-01-15T10:00:00Z"
}
CREDS

RUN chmod 0666 /home/user/credentials/creds.json || true

RUN cat <<'SCHEMA' > /home/user/credentials/creds_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Credentials Schema",
  "type": "object",
  "required": ["user", "access_key", "secret_key", "rotation_date"],
  "properties": {
    "user":          { "type": "string" },
    "access_key":    { "type": "string" },
    "secret_key":    { "type": "string" },
    "rotation_date": { "type": "string", "format": "date-time" }
  },
  "additionalProperties": false
}
SCHEMA

RUN chmod 0644 /home/user/credentials/creds_schema.json && \
    chmod 755 /home/user