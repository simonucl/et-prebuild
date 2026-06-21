FROM ubuntu:22.04

# Labels
LABEL Author="Container Builder"
LABEL Description="Docker image for jq filtering task with pytest pre-installed."

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create training_samples.json
RUN cat > /home/user/data/training_samples.json <<'JSON'
[
  {"id":"001","features":[0.1,0.5,0.2],"label":"positive"},
  {"id":"002","features":[0.3,0.6],"label":"negative"},
  {"id":"003","features":[0.4,0.2,0.1],"label":"neutral"},
  {"id":"004","features":[0.8,0.9,0.7],"label":"negative"},
  {"id":"005","id_extra":"something","features":[0.2,0.4,0.5],"label":"positive"}
]
JSON

# Create feature_schema.json
RUN cat > /home/user/data/feature_schema.json <<'JSON'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "features", "label"],
  "properties": {
    "id":  { "type": "string" },
    "features": {
      "type": "array",
      "items": { "type": "number" },
      "minItems": 3,
      "maxItems": 3
    },
    "label": {
      "type": "string",
      "enum": ["positive", "negative"]
    }
  },
  "additionalProperties": true
}
JSON

# Ensure correct ownership for the non-root user
RUN chown -R user:user /home/user

# Environment variables
ENV HOME=/home/user
ENV PATH=$PATH:/home/user/.local/bin

# Set permissions on home directory
RUN chmod 755 /home/user

# Default command
CMD ["/bin/bash"]