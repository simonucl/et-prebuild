FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer setup"
LABEL Description="Container image supplying initial state for the log-extraction exercise."

# Update base system and install Python + pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the directory structure
RUN mkdir -p /home/user/data

# Populate the pre-existing log file with the required 10 lines
RUN cat > /home/user/data/server.log <<'EOF'
2024-04-21 14:03:22 [INFO] Starting server
2024-04-21 14:03:23 [WARN] Low disk space
2024-04-21 14:03:25 [CRITICAL] Database connection failed
2024-04-21 14:03:26 [INFO] Retrying connection
2024-04-21 14:03:28 [CRITICAL] Database connection failed
2024-04-21 14:04:01 [ERROR] Could not write to log
2024-04-21 14:05:12 [FATAL] Kernel panic
2024-04-21 14:06:30 [INFO] Shutdown initiated
2024-04-21 14:06:35 [FATAL] Unable to recover
2024-04-21 14:06:40 [INFO] Shutdown complete
EOF

# Ensure correct permissions
RUN chmod 0644 /home/user/data/server.log && \
    chmod 0777 /home/user/data && \
    chmod 0755 /home/user

# Guarantee that none of the solution files exist in the base image
RUN rm -f /home/user/data/extract_cf.sh \
          /home/user/data/critical_fatal.log \
          /home/user/data/summary.txt

# Environment variables
ENV LC_ALL=C
ENV LANG=C