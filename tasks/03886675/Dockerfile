FROM ubuntu:22.04

# Install Python, pip, pytest, create home, cleanup
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Run script equivalent
CMD ["/bin/bash", "-c", "echo 'Container for root-UID sanity-check exercise.  Invoke your commands inside an interactive shell:'; exec /bin/bash"]