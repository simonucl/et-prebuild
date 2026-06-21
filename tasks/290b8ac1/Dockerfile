FROM ubuntu:22.04

# Labels
LABEL Author="task-prep"
LABEL Description="Container image for the \"deployment log extraction\" task."

# Update and install Python + pytest
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create deployment directory structure
RUN mkdir -p /home/user/deployment

# Populate the raw deployment log with the exact canonical content
RUN cat > /home/user/deployment/app_update.log << 'EOF'
[2023-05-01 10:00:00] INFO Starting deployment v2.3.4
[2023-05-01 10:00:01] ERROR Failed to backup config for v2.3.4
[2023-05-01 10:00:02] WARNING Low disk space on /dev/sda1
[2023-05-01 10:00:03] ERROR Dependency mismatch v2.3.3
[2023-05-01 10:00:04] INFO Copying binaries v2.3.4
[2023-05-01 10:00:05] ERROR Timeout while restarting service v2.3.4
[2023-05-01 10:00:06] INFO Deployment finished v2.3.4
[2023-05-01 10:00:07] ERROR Rollback triggered v2.3.4
[2023-05-01 10:00:08] INFO Cleanup complete
EOF

# Ensure the directory is writable by the non-root runtime user
RUN chmod -R a+rwX /home/user/deployment && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin