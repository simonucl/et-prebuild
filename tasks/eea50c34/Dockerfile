FROM ubuntu:22.04

# Labels
LABEL Author="setup-script"
LABEL Description="Container for checksum monitoring task (pytest pre-state ensured)"

# Update package list and install Python + pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Add a non-privileged user named "user"
RUN useradd -m -s /bin/bash user || true

# Create directories
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/alerts && \
    chmod 0755 /home/user/data && \
    chmod 0755 /home/user/alerts

# Initial configuration file with exact content and a trailing newline
RUN cat > /home/user/data/critical_config.cfg <<'EOF'
DB_HOST=localhost
DB_PORT=5432
DB_USER=monitor
DB_PASS=monitor123
EOF

RUN chmod 0644 /home/user/data/critical_config.cfg

# Ensure the "user" account owns its home directory tree
RUN chown -R user:user /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin