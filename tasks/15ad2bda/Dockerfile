FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Container for firewall rule manifest exercise with pytest installed."

# %post section
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment-time chmod requirement
RUN chmod 755 /home/user

# %environment section variables
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin