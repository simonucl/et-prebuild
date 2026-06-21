FROM ubuntu:22.04

# Labels
LABEL Author="AI Container Builder"
LABEL Description="Environment for release-manager frequency report exercise with pytest pre-installed."

# Update package lists and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential \
        locales && \
    pip3 install --no-cache-dir --upgrade pytest && \
    ln -sf /usr/bin/python3 /usr/local/bin/python

# Create the required directory structure
RUN mkdir -p /home/user/releases

# Create the input file
RUN cat >/home/user/releases/services_2023-10.txt <<'EOF'
auth
billing
auth
reports
auth
billing
search
search
analytics
EOF

# Ensure correct permissions and clean up
RUN chmod 755 /home/user/releases && \
    chmod 644 /home/user/releases/services_2023-10.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:$PATH"