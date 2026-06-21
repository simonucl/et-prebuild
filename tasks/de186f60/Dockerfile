FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Prep"
LABEL Description="Base image for the People → Department ETL CLI exercise."

# Update package lists and install needed CLI tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test-runner
RUN pip3 install --no-cache-dir pytest

# Create working directory structure
RUN mkdir -p /home/user/data_pipeline

# Pre-seed the initial data files expected by the exercise
# 1. employees.json (must include terminating LF)
RUN cat > /home/user/data_pipeline/employees.json << 'EOF'
[
  {"id": 1, "name": "Alice", "department_id": 1},
  {"id": 2, "name": "Bob", "department_id": 2},
  {"id": 3, "name": "Carol", "department_id": 2},
  {"id": 4, "name": "Dave", "department_id": 3}
]
EOF

# 2. employees_schema.json (must include terminating LF)
RUN cat > /home/user/data_pipeline/employees_schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "name", "department_id"],
    "properties": {
      "id": { "type": "integer" },
      "name": { "type": "string" },
      "department_id": { "type": "integer" }
    },
    "additionalProperties": false
  }
}
EOF

# Permissions: make sure the non-root user on the host can write
# into /home/user/data_pipeline to create the required artefacts.
RUN chmod -R 0777 /home/user/data_pipeline

# Set permissions for home directory and environment variables
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

WORKDIR /home/user/data_pipeline