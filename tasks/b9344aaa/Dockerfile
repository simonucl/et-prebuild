FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Container for backup-archive task with pytest pre-installed"

# Update package lists and install Python + pip
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

# Install pytest for test execution
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/test_configs

# Create the required configuration files with exact contents
RUN cat > /home/user/test_configs/config1.ini <<'EOF'
[database]
host=localhost
port=5432
EOF

RUN cat > /home/user/test_configs/config2.ini <<'EOF'
[web]
host=0.0.0.0
port=8080
EOF

# Ensure permissive permissions so the non-root agent user can write
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Help information (as comment):
# This container image provides the initial state for the backup-archive
# exercise. The directory /home/user/test_configs/ contains two INI files
# that the learner must archive. Pytest is installed so the automated
# grading harness can run its tests.