# Using ubuntu:22.04 because localimage cannot be used in Docker
FROM ubuntu:22.04

# Install required software
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync && \
    pip3 install --no-cache-dir pytest

# Create initial filesystem layout for the task
RUN set -e && \
    mkdir -p /home/user/edge_source && \
    printf 'print("Edge app v1.1.0")\n'  > /home/user/edge_source/app.py && \
    printf '1.1.0\n'                    > /home/user/edge_source/version.txt && \
    printf 'setting: prod\n'            > /home/user/edge_source/config.yaml && \
    mkdir -p /home/user/iot_device/edge_app && \
    printf 'print("Edge app v1.0.0")\n' > /home/user/iot_device/edge_app/app.py && \
    printf '1.0.0\n'                    > /home/user/iot_device/edge_app/version.txt && \
    printf 'legacy\n'                   > /home/user/iot_device/edge_app/old.tmp && \
    rm -rf /home/user/deployment_logs && \
    chmod -R a+rwx /home/user

# Equivalent to %runscript
CMD chmod 755 /home/user && echo "IoT sync task container. Opening interactive shell..." && exec /bin/bash