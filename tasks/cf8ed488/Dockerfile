FROM ubuntu:22.04

# Make apt non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update index and install Python + pip
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the validation framework
RUN pip3 install --no-cache-dir pytest

# Create the base directory structure
RUN mkdir -p /home/user/container_debug/logs

# Ensure correct permissions
RUN chmod 755 /home/user/container_debug/logs && \
    chmod 755 /home/user/container_debug && \
    chmod 755 /home/user

# Create the log file with exact content
RUN cat >/home/user/container_debug/logs/app_container_01.log <<'EOF'
2023-08-01 10:02:15 INFO App started
2023-08-01 10:03:47 WARN Low memory
2023-08-01 10:05:03 ERROR NullPointerException at line 42
2023-08-01 10:07:11 INFO Processing request id=123
2023-08-01 10:08:54 ERROR IndexOutOfBoundsException at line 87
2023-08-01 10:09:33 INFO Request completed id=123
2023-08-01 10:11:22 ERROR Failed to connect to database
2023-08-01 10:12:45 INFO App terminated
EOF

# Set the required permissions on the log file
RUN chmod 644 /home/user/container_debug/logs/app_container_01.log

# Keep a clean PATH that includes Python binaries
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Set the default command
CMD ["bash", "-c", "echo 'Container for log-processing task. Open a shell to begin.' >&2 && exec /bin/bash"]