FROM ubuntu:22.04

# System packages and Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create unprivileged user
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true

# Populate immutable source tree
RUN mkdir -p /home/user/data_source/docs && \
    mkdir -p /home/user/data_source/media && \
    mkdir -p /home/user/data_source/configs

RUN printf 'Project Documentation v1.0\n' > /home/user/data_source/docs/readme.txt && \
    printf '# User Guide\n' > /home/user/data_source/docs/guide.md

RUN printf 'fakejpgdata1\n' > /home/user/data_source/media/photo1.jpg && \
    printf 'fakepngdata2\n' > /home/user/data_source/media/photo2.png

RUN printf 'port=8080\n' > /home/user/data_source/configs/app.conf

# Optional empty backup root directory
RUN mkdir -p /home/user/backup_archive

# Ownership and permissions
RUN chown -R 1000:1000 /home/user && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/backup_archive

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Labels
LABEL Author="Task setup: Backup Administrator Scenario"
LABEL Description="Container prepared for the backup-archive symbolic-link task with pytest preinstalled."