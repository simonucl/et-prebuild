FROM ubuntu:22.04

# Help:
# This container provides the initial state for the credential rotation
# exercise.
#   • /home/user/web/credentials.html          (pre-seeded HTML snippet)
#   • Python 3 and pytest                      (for automated grading)
#   • curl and w3m                             (optional scraping tools)

ENV HOME=/home/user

RUN set -e && \
    echo "Updating apt cache and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        w3m \
        ca-certificates && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory structure and seed files..." && \
    mkdir -p /home/user/web && \
    chmod 0777 /home/user

RUN cat > /home/user/web/credentials.html <<'EOF'
<div id="current-user">new_admin</div>
EOF

RUN chmod 0644 /home/user/web/credentials.html && \
    echo "Cleanup APT caches to keep the image small..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

LABEL Author="Automatic build for credential-rotation task"
LABEL Description="Container with preset credential HTML and pytest installed"