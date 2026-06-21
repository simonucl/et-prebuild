# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section (from .def file)
# Basic tooling, seed files, and user environment setup for assignment

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest jsonschema && \
    mkdir -p /home/user/build

RUN cat >/home/user/build/artifacts.json <<'EOF'
[
  {
    "name": "libwidget",
    "version": "1.2.3",
    "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
  },
  {
    "name": "libgizmo",
    "version": "4.5.6",
    "sha256": "2222222222222222222222222222222222222222222222222222222222222222"
  },
  {
    "name": "app-thing",
    "version": "0.9.1",
    "sha256": "3333333333333333333333333333333333333333333333333333333333333333"
  }
]
EOF

RUN cat >/home/user/build/artifact_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["name", "version", "sha256"],
    "properties": {
      "name":    { "type": "string", "minLength": 1 },
      "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
      "sha256":  { "type": "string", "pattern": "^[a-f0-9]{64}$" }
    },
    "additionalProperties": false
  }
}
EOF

RUN chmod -R a+rwX /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV HOME="/home/user"

RUN chmod 755 /home/user