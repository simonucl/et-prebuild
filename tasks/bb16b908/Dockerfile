FROM ubuntu:22.04

# Set environment variables
ENV HOME=/home/user

# Update apt index and install Python + pip
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

# Install pytest (required by the grading harness)
RUN pip3 install --no-cache-dir pytest

# Create /home/user with write permissions so the unprivileged runtime user
# can create additional files/directories such as /home/user/compliance/.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create the repository layout and configuration files.
RUN mkdir -p /home/user/repo/config

# Create sshd_config
RUN cat > /home/user/repo/config/sshd_config <<'EOF'
# OpenSSH server configuration
Port 22
Protocol 2
PasswordAuthentication yes
# allow root login
PermitRootLogin yes
ChallengeResponseAuthentication no
EOF

# Create sshd_config_alt
RUN cat > /home/user/repo/config/sshd_config_alt <<'EOF'
# Alternative config
Port 2222
Protocol 2
PermitRootLogin no
EOF

# Ensure repository files are readable
RUN chmod -R a+r /home/user/repo && \
    chmod 755 /home/user

# Labels
LABEL Author="DevSecOps-PolicyTask"
LABEL Description="Container for policy-as-code compliance automation task."

# Set working directory
WORKDIR /home/user

# Help information (as comment):
# This container provides the initial repository layout required for the
# "policy-as-code" task.  Pytest is pre-installed so the grading harness can
# execute its test-suite.  The runtime user is expected to create
# /home/user/compliance/root_login_findings.log as described in the assignment.