# Converted from Apptainer definition using ubuntu:22.04 equivalent
FROM ubuntu:22.04

# Install Python tooling and DNS utilities
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip dnsutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/project-lambda && \
    chmod -R 0777 /home/user/projects && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Original runscript message
CMD echo "Container for the DNS lookup helper exercise. Use 'docker run' or 'docker exec' to work inside the image."