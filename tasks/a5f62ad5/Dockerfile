FROM ubuntu:22.04

# Labels
LABEL Author="AI_Apptainer_Agent"
LABEL Description="Base image for 'tiny build system' task with initial filesystem state"

# Post section
RUN set -e \
    && echo "Updating package index and installing required packages..." \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends make python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest via pip..." \
    && pip3 install --no-cache-dir pytest

RUN echo "Setting up directory structure and dummy log files..." \
    && mkdir -p /home/user/disk_admin/reports \
    && chmod -R 0777 /home/user \
    && printf "dummy1\n" > /home/user/disk_admin/reports/old_app1.log \
    && printf "dummy2\n" > /home/user/disk_admin/reports/old_app2.log \
    && chmod 666 /home/user/disk_admin/reports/old_app1.log \
    && chmod 666 /home/user/disk_admin/reports/old_app2.log \
    && echo "Initial setup complete. The archives directory, Makefile, and generated report files are intentionally absent."

# Environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
RUN chmod 755 /home/user

# Runscript (converted to comments)
# Container for the 'tiny build system' task.
# To start working, open a shell inside the container:
#     docker run -it <image> /bin/bash