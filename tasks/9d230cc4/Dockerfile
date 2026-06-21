FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Create a writable home directory for the non-root user that will run the tasks
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply permissions referenced in %labels section
RUN chmod 755 /home/user

LABEL Author="cloud-migration-container"
LABEL Description="Clean environment for cloud-migration task with pytest installed."

CMD ["bash"]