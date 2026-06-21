FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    rm -rf /var/lib/apt/lists/*

# Ensure Python and pip are on PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default action prints Python and pytest versions
CMD ["sh", "-c", "python3 --version && pytest --version"]