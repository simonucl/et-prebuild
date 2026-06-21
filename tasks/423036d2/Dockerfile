FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create initial ETL project skeleton expected by the grader
RUN mkdir -p /home/user/etl_project/load

# extract.py (exactly 5 lines, including blank line)
RUN cat > /home/user/etl_project/extract.py <<'PY'
def extract():
    print("extract step")

if __name__ == "__main__":
    extract()
PY

# transform.py (hard-coded secret on line 3 to be flagged later)
RUN cat > /home/user/etl_project/transform.py <<'PY'
def transform():

    aws_secret = "AKIAFAKESECRET123"    # <- THIS SHOULD BE FLAGGED
    print("transform step")

if __name__ == "__main__":
    transform()
PY

# load/loader.py (exactly 3 lines, including trailing blank line)
RUN cat > /home/user/etl_project/load/loader.py <<'PY'
def load():
    print("load step")

PY

# README.md
RUN cat > /home/user/etl_project/README.md <<'EOF'
# Demo ETL project

This repository contains a toy Extract-Transform-Load (ETL) pipeline used for
training and automated assessment.
EOF

# Ensure the agent (non-root) can modify the project files
RUN chmod -R a+rwX /home/user/etl_project

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Labels
LABEL Author="example"
LABEL Description="Ubuntu 22.04 base with starter ETL project and pytest pre-installed"