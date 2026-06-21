FROM ubuntu:22.04

# Help section not provided in source

ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

RUN chmod 755 /home/user || true

RUN set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && pip3 install --no-cache-dir pytest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/diagnostics

RUN printf 'abc' > /home/user/diagnostics/app.log \
    && chmod 0644 /home/user/diagnostics/app.log

RUN chmod 0777 /home/user/diagnostics