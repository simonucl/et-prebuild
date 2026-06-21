# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python, pip, pytest, and cleanup
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create user with UID/GID 1000
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Create project structure
RUN PROJECT_DIR=/home/user/project && \
    mkdir -p "$PROJECT_DIR/src" && \
    printf 'Demo project for packaging\n' > "$PROJECT_DIR/README.md" && \
    printf 'print("Hello, packaged world!")\n' > "$PROJECT_DIR/src/main.py" && \
    chown -R 1000:1000 /home/user

# Environment setup actions that modify system state
RUN chmod 755 /home/user && \
    if [ -x /usr/bin/python3 ] && [ ! -e /usr/bin/python ]; then \
        ln -s /usr/bin/python3 /usr/bin/python; \
    fi

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Labels
LABEL Author="AI-Generated"
LABEL Description="Container for packaging workflow task – includes toy project and pytest"