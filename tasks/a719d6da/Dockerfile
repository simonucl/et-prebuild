FROM ubuntu:22.04

# Update package lists and install essential tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment-time permissions adjustment
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

# Runscript equivalent
CMD ["sh", "-c", "echo \"Container for system-diagnostics assignment. Open a shell to begin.\""]