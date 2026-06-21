FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Initial state for API latency CSV manipulation exercise"

# Update package index and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the user home hierarchy
RUN mkdir -p /home/user/api_test/logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/api_test && \
    chmod 755 /home/user/api_test/logs

# Create the log file with exactly five lines and a trailing newline
RUN cat >/home/user/api_test/logs/api_responses_20240314.log <<'EOF'
2024-03-14T07:21:01Z,GET,/users,200,115ms
2024-03-14T07:22:45Z,POST,/login,201,89ms
2024-03-14T07:23:50Z,DELETE,/users/42,204,102ms
2024-03-14T07:24:30Z,GET,/reports,500,321ms
2024-03-14T07:25:10Z,PUT,/users/42,404,78ms
EOF

# Set the exact permissions required by the tests
RUN chmod 644 /home/user/api_test/logs/api_responses_20240314.log

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Python binaries installed via pip are discoverable
ENV PATH="$PATH:/usr/local/bin"

# Help information (as comments):
# This Docker image provides the starting environment for the
# API latency processing task.  It contains:
#   • The raw log file in /home/user/api_test/logs/
#   • Python and pytest pre-installed for automated grading.