FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container image pre-configured for the log analysis shell task. Includes pytest and initial log data."

# Install Python3, pip and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the user's home directory hierarchy
RUN mkdir -p /home/user/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/logs

# Populate /home/user/logs/user_actions.log with the exact 10 lines
RUN cat > /home/user/logs/user_actions.log <<'EOF'
2024-05-18 08:14:22 alice LOGIN
2024-05-18 08:16:30 bob LOGIN
2024-05-18 08:20:44 alice LOGOUT
2024-05-18 09:01:07 charlie FAILED
2024-05-18 09:02:12 diana LOGIN
2024-05-18 09:05:55 charlie LOGIN
2024-05-18 09:07:01 charlie LOGOUT
2024-05-18 09:10:33 bob LOGOUT
2024-05-18 09:11:11 edward LOGIN
2024-05-18 09:15:00 frank FAILED
EOF

RUN chmod 0644 /home/user/logs/user_actions.log

# Intentionally DO NOT create /home/user/reports – the student must
# create it during task execution.

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user