FROM ubuntu:22.04

# Help:
# This Apptainer image provides the starting filesystem state for the
# IoT-edge firmware packaging exercise and includes pytest for validation.

ENV HOME=/home/user

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/iot_workdir/source/edge

RUN printf 'The quick brown fox jumps over the lazy dog' \
        > /home/user/iot_workdir/source/edge/firmware_v2.3.1.bin

RUN cat >/home/user/iot_workdir/source/edge/config.yaml <<'EOF'
---
version: "2.3.1"
device: "EDGE-NODE-A1"
features:
  - gpio
  - ble
  - wifi
...
EOF

RUN echo 'MIT License' > /home/user/iot_workdir/source/edge/LICENSE.txt

RUN chmod -R a+rwx /home/user

# Labels (converted from %labels)
LABEL Author="Container build script for IoT-edge firmware task"