FROM ubuntu:22.04

LABEL Author="Apptainer Task Setup"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        dnsutils \
        curl \
        wget \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip setuptools && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0775 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", "chmod 755 /home/user && echo 'Container for migration diagnostics lab. Execute your commands as needed.'"]