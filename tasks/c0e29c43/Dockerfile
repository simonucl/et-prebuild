# syntax=docker/dockerfile:1
# Converted from Apptainer definition file

FROM ubuntu:22.04

# Help section
# Container for DNS report task. Use 'apptainer exec ...' to run commands inside.

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libnss-systemd \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    if ! grep -qE 'hosts:.*myhostname' /etc/nsswitch.conf; then \
        sed -i 's/^\(hosts:.*\)/\1 myhostname/' /etc/nsswitch.conf; \
    fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure correct permissions
RUN chmod 755 /home/user

CMD echo "Container for DNS report task. Use 'docker run ...' to run commands inside."