FROM ubuntu:22.04

# Author server_reports_container_setup
# Description "Base image for the 'server_reports' exercise. Provides Python, pytest, jq and a writable workspace at /home/user."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest jsonschema && \
    mkdir -p /home/user/server_reports && \
    chmod 0777 /home /home/user /home/user/server_reports && \
    chmod 755 /home/user

ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD echo "This container is ready for the 'server_reports' exercise." && \
    echo "A writable workspace is available at /home/user/server_reports." && \
    echo "Use 'pytest' to run the assessment tests."