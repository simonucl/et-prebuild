FROM ubuntu:22.04

# Install Python tooling for the grader
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up initial filesystem state for the mini-firewall exercise
RUN mkdir -p /home/user/firewall_task

# Seed firewall.rules with the original rule set (only port 80 allowed)
RUN cat > /home/user/firewall_task/firewall.rules <<'EOF'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p tcp --dport 80 -j ACCEPT
COMMIT
EOF

# Simple placeholder README
RUN echo "This is a placeholder README for the mini-firewall task." \
    > /home/user/firewall_task/README.txt

# Permissions
# Directory must be writable so the non-root learner can create files.
RUN chmod 777 /home/user/firewall_task

# Learner needs to modify firewall.rules; make it world-writable.
RUN chmod 666 /home/user/firewall_task/firewall.rules

# README need not be writable, but keep it world-readable.
RUN chmod 644 /home/user/firewall_task/README.txt

# Set home directory permissions
RUN chmod 755 /home/user

# Labels
LABEL Author="ChatGPT"
LABEL Description="Container for the mini-firewall editing exercise."

# Help:
# This container image contains the initial project files and Python testing
# tools for the "mini-firewall" task.