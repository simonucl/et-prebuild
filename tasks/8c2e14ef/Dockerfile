FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial filesystem state expected by tests
RUN set -eux && \
    mkdir -p /home/user/project_files && \
    printf 'Hello Backup\n'        > /home/user/project_files/file1.txt && \
    printf 'Data Integrity Test\n' > /home/user/project_files/file2.txt && \
    rm -rf /home/user/backups && \
    chmod -R a+rX,u+w /home/user

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

LABEL Author="Container Build Script"
LABEL Description="Apptainer image for backup integrity task with pytest pre-installed"