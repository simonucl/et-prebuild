# Converted from Apptainer .def
FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container for security-permissions sweep task with pytest installed."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create project structure
RUN mkdir -p /home/user/my_app/scripts && \
    touch /home/user/my_app/deploy.sh && chmod 777 /home/user/my_app/deploy.sh && \
    touch /home/user/my_app/scripts/cleanup.sh && chmod 777 /home/user/my_app/scripts/cleanup.sh

# Create build.sh via heredoc
RUN cat << 'EOF' > /home/user/my_app/scripts/build.sh
#!/bin/bash
echo "Building project"
EOF

# Permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/my_app && \
    chmod 755 /home/user/my_app/scripts && \
    chmod 755 /home/user/my_app/scripts/build.sh

ENV HOME=/home/user