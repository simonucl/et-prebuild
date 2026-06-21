FROM ubuntu:22.04

# Labels
LABEL Author="task-preparer"
LABEL Description="Container image for support-engineer log analysis task."

# Install Python tooling
RUN set -e && \
    echo "Updating apt repositories and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user 'user' with home directory /home/user
RUN echo "Creating non-root user 'user' with home directory /home/user ..." && \
    useradd -m -s /bin/bash user

# Install pytest for the runtime user
RUN echo "Installing pytest for the runtime user..." && \
    pip3 install --no-cache-dir pytest

# Setting up initial support log files
RUN mkdir -p /home/user/support/logs

# Create app.log file
RUN cat >/home/user/support/logs/app.log <<'EOF'
[2023-07-01 10:00:01] INFO Starting service
[2023-07-01 10:01:15] ERROR Failed to connect to database
[2023-07-01 10:02:20] WARN Low disk space
[2023-07-01 10:03:25] INFO Service running
[2023-07-01 10:04:30] ERROR Timeout while reading response
EOF

# Create app2.log file
RUN cat >/home/user/support/logs/app2.log <<'EOF'
2023-07-01T11:00:00Z INFO scheduled job start
2023-07-01T11:00:05Z ERROR job crashed with code 1
2023-07-01T11:00:10Z INFO scheduled job end
2023-07-01T11:05:00Z ERROR unable to send email
EOF

# Ensure correct ownership so the non-root runtime user can read/write
RUN chown -R user:user /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash", "-c", "echo 'Container for support-engineer task.' && echo 'Switch to the user account to work.' && /bin/bash"]