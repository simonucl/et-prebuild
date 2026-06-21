FROM ubuntu:22.04

# Install Python tooling for test execution
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure and initial CSV file
RUN mkdir -p /home/user/security

RUN cat > /home/user/security/services.csv <<'EOF'
service,status
cups,disable
ssh,enable
avahi-daemon,disable
bluetooth,disable
ntp,enable
EOF

# Set correct permissions
RUN chmod 0644 /home/user/security/services.csv
RUN chmod 0755 /home/user/security
RUN chmod 755 /home/user

# Labels
LABEL Author="container-builder"
LABEL Description="Environment for the 'security hardening' task with initial CSV data and pytest installed."

# Environment variables
ENV PATH="$PATH:/usr/local/bin"

# Run script equivalent
CMD ["/bin/sh", "-c", "echo 'Container built for the security hardening task. Execute your commands manually.'"]