FROM ubuntu:22.04

# Author Release-Check Exercise
# Description Base image for DNS sanity-check task (pytest pre-installed)

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python-is-python3 \
    ca-certificates

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 755 /home/user && chown -R 1000:1000 /home/user || true

RUN rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]