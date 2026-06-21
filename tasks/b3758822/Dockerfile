FROM ubuntu:22.04

# Update package index and install required tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        tar

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create the directory structure expected by the grading tests
RUN mkdir -p /home/user/apps/app_v1.1 && \
    mkdir -p /home/user/deployment_logs && \
    mkdir -p /home/user/update_packages

# Populate version 1.1 of the application
RUN echo "print('Hello from version 1.1')" > /home/user/apps/app_v1.1/app.py && \
    echo "config: v1.1" > /home/user/apps/app_v1.1/config.yml && \
    echo "Version 1.1 of the application." > /home/user/apps/app_v1.1/README.md && \
    printf "v1.1\n" > /home/user/apps/app_v1.1/VERSION

# Create the symbolic link /home/user/apps/current → .../app_v1.1
RUN ln -s /home/user/apps/app_v1.1 /home/user/apps/current

# Prepare the update package tarball for version 1.2
RUN mkdir -p /tmp/app_v1.2 && \
    echo "print('Hello from version 1.2')" > /tmp/app_v1.2/app.py && \
    echo "config: v1.2" > /tmp/app_v1.2/config.yml && \
    echo "Version 1.2 of the application." > /tmp/app_v1.2/README.md && \
    printf "v1.2\n" > /tmp/app_v1.2/VERSION

# Pack the directory into app_v1.2.tar.gz (must contain app_v1.2/…)
RUN tar -C /tmp -czf /home/user/update_packages/app_v1.2.tar.gz app_v1.2

# Clean up the temporary build directory
RUN rm -rf /tmp/app_v1.2

# Set permissive permissions so the unprivileged grader/agent can write
RUN chmod -R 777 /home/user/apps && \
    chmod -R 777 /home/user/deployment_logs && \
    chmod -R 777 /home/user/update_packages && \
    chmod 755 /home/user

# Labels
LABEL Author="devops-automation-setup"