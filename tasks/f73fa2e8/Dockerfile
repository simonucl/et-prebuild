# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update package lists and install required tools
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Create a writable home directory for the unprivileged agent
RUN mkdir -p /home/user && chmod 0777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# Label
LABEL Author="deployment-task"

# Run script
CMD ["bash"]