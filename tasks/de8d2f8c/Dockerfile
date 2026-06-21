FROM ubuntu:22.04

LABEL Author="Docker-Expert"
LABEL Description="Base image for diagnostics-logging exercise. Pytest installed; writable /home/user prepared."

# Update package lists and install Python and pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Prepare writable home directory for the non-root user who will run the container
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Set environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Set working directory
WORKDIR /home/user

CMD ["echo", "Container for diagnostics-logging task. This image is intended to be used by the automated grader."]