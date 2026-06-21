FROM ubuntu:22.04

# Labels
LABEL Author="Automated Setup"
LABEL Description="Base image for \"weekday docs build\" cron-job task."

# Install required system packages and Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install \
        cron \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem skeleton expected by the tests
RUN mkdir -p /home/user/scripts && \
    mkdir -p /home/user/logs

# Create dummy build script that the future cron job will call
RUN cat > /home/user/scripts/build_docs.sh <<'EOF'
#!/bin/bash
#
# Placeholder documentation build script.
# Emits a timestamped message so that log appends are visible.
echo "[`date +'%Y-%m-%d %H:%M:%S'`] docs build stub executed"
EOF

RUN chmod 755 /home/user/scripts/build_docs.sh

# Pre-existing log file that the cron job will append to
RUN touch /home/user/logs/build_docs.log && \
    chmod 666 /home/user/logs/build_docs.log

# Directory permissions: make sure the unprivileged test runner can write
RUN chmod 777 /home/user/logs && \
    chmod 755 /home/user/scripts && \
    chmod 755 /home/user

# Default entrypoint: open an interactive shell
CMD ["/bin/bash"]