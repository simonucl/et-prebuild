FROM ubuntu:22.04

# Help section from Apptainer %help was not provided

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        cron && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

CMD ["/bin/bash"]