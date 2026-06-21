# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create project structure
RUN mkdir -p /home/user/project/src

# main.py
RUN cat > /home/user/project/src/main.py <<'EOF'
# main module
def hello():
    print("Hello from main")
EOF

# utils.py
RUN cat > /home/user/project/src/utils.py <<'EOF'
# utility module
def add(a, b):
    return a + b
EOF

# README.md
RUN cat > /home/user/project/README.md <<'EOF'
Sample project directory. Do not archive me!
EOF

# Ensure write permissions
RUN chmod -R 0777 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV PYTHONIOENCODING=utf-8

# Additional environment setup
RUN chmod 755 /home/user

# Run script
CMD ["bash", "-c", "exec \"$@\"", "--"]