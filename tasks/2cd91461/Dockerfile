FROM ubuntu:22.04

# Help / label information derived from %labels
# chmod 755 /home/user
LABEL Author="AI-generated compliance task base image"

RUN set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cron \
        python3-pip \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user \
    && chmod 0777 /home/user \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*