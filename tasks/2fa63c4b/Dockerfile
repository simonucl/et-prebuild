FROM ubuntu:22.04

# Author: Apptainer Task Builder
# Description: Container for automated QA checksum verification task.

ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/qa_resources && \
    chmod 755 /home/user/qa_resources && \
    touch /home/user/qa_resources/patch_release_v1.0.0.zip && \
    truncate -s 0 /home/user/qa_resources/patch_release_v1.0.0.zip

RUN apt-get clean && rm -rf /var/lib/apt/lists/*