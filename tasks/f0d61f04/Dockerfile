FROM ubuntu:22.04

# Author Performance-Tuning Exercise
LABEL Author="Performance-Tuning Exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -d /home/user -u 1000 -g user user; \
    fi

RUN mkdir -p /home/user/samples

RUN echo 'exec_time_ms=250' > /home/user/samples/webserver.log
RUN echo 'exec_time_ms=75'  > /home/user/samples/cache.log
RUN echo 'exec_time_ms=184' > /home/user/samples/db.log

RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/samples && \
    chmod 644 /home/user/samples/*.log