FROM ubuntu:22.04

# Help: runscript executes passed command
# No user creation specified; using root with adjusted permissions

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/workflows/input

RUN printf '{"name": "serviceA", "enabled": true}\n' \
        > /home/user/workflows/input/config1.json && \
    printf '{"name": "serviceB", "enabled": false}\n' \
        > /home/user/workflows/input/config2.json && \
    printf '{"name": "serviceC", "enabled": true}\n' \
        > /home/user/workflows/input/config3.json

RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["bash"]