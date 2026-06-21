FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for the tiny firewall exercise with pytest pre-installed."

# %environment converted to ENV
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create filesystem layout
RUN mkdir -p /home/user/firewall && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/firewall

# Create rules.conf containing "#\n"
RUN printf '#\n' > /home/user/firewall/rules.conf && \
    chmod 0666 /home/user/firewall/rules.conf

# Apply permissions from %environment
RUN chmod 755 /home/user