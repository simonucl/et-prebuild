FROM ubuntu:22.04

# Labels
LABEL Maintainer="network-disk-audit exercise"
LABEL Description="Base image for Disk Usage Audit task – provides pytest and writable /home/user."

# Update package lists and install Python package manager
RUN apt-get update -y && \
    apt-get install -y python3-pip

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Prepare the required home directory for the learner
# Give broad write permissions so whichever UID runs the container can work there
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD echo "Container for Disk Usage Audit task is ready." && echo "Your workspace is /home/user"