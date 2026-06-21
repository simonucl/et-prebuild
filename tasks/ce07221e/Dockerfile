FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Image prepared for configuration-management toggle task with pytest pre-installed."

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Update package lists and install Python and tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/configs

# Populate the initial configuration file with the exact contents
RUN cat > /home/user/configs/app.cfg <<'EOF'
# Application Configuration
VERSION=1.4.2
ENABLED=false
LOG_LEVEL=info
EOF

# Set reasonable permissions so the unprivileged agent can read/write
RUN chmod 755 /home/user && \
    chmod 755 /home/user/configs && \
    chmod 644 /home/user/configs/app.cfg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Help information (as comments):
# This image provides the initial state required for the
# configuration-management audit exercise. It contains:
#   • /home/user/configs/app.cfg with ENABLED=false
#   • Python and pytest for automated grading