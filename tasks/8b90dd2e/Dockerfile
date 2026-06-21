FROM ubuntu:22.04

# Help:
# This container provides a clean Ubuntu 22.04 environment with Python 3 and
# pytest pre-installed. No monitoring configuration files are present so that
# students can complete the assignment from a pristine starting state.

LABEL Author="Apptainer Task Setup"
LABEL Description="Base container for monitoring configuration exercise with pytest installed."

ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*