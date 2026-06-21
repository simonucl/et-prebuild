FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Base image for stub-API exercise – provides curl, Python, and pytest, but leaves the required exercise artefacts absent."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Apply environment-time home permissions
RUN chmod 755 /home/user

CMD ["/bin/bash"]