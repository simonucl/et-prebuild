FROM ubuntu:22.04

# Labels
LABEL Author="task-setup"
LABEL Description="Environment for quick security-keyword sweep task"

# Update package lists and install Python & pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create the demo project exactly as described in the task statement
RUN mkdir -p /home/user/projects/app

# /home/user/projects/app/main.py
RUN cat >/home/user/projects/app/main.py <<'EOF'
# Sample app
def login():
    # TODO: improve security
    password = "12345"
EOF

# /home/user/projects/app/utils.py
RUN cat >/home/user/projects/app/utils.py <<'EOF'
# utility
secret_key = "abcde"
def helper():
    pass
EOF

# Ensure the agent (non-root at runtime) can create new directories/files
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home/user