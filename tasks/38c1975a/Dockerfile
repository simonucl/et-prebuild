FROM ubuntu:22.04

# Install required system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create user and group
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g user -s /bin/bash user

# Create data directory
RUN install -d -m 0755 /home/user/data

# Write inventory.json
RUN cat > /home/user/data/inventory.json <<'EOF'
{
  "warehouse": "central",
  "items": [
    {"id":101,"name":"blue widget","quantity":5},
    {"id":102,"name":"red widget","quantity":25},
    {"id":203,"name":"green gizmo","quantity":7},
    {"id":304,"name":"yellow gizmo","quantity":12}
  ]
}
EOF

# Write inventory_schema.json
RUN cat > /home/user/data/inventory_schema.json <<'EOF'
{
  "$schema":"http://json-schema.org/draft-07/schema#",
  "type":"object",
  "required":["warehouse","items"],
  "properties":{
    "warehouse":{"type":"string"},
    "items":{
      "type":"array",
      "items":{
        "type":"object",
        "required":["id","name","quantity"],
        "properties":{
          "id":{"type":"integer"},
          "name":{"type":"string"},
          "quantity":{"type":"integer","minimum":0}
        }
      }
    }
  }
}
EOF

# Fix ownership and permissions
RUN chown -R 1000:1000 /home/user && \
    chmod 0755 /home/user/data

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/user/.local/bin

# Ensure home permissions match original intent
RUN chmod 755 /home/user

# Help text (from %runscript)
# This container is prepared for the inventory validation task.
# Invoke your commands manually inside an interactive shell.

CMD ["/bin/bash"]