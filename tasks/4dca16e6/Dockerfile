FROM ubuntu:22.04

# Help / labels
LABEL Author="Config-Manager Task Environment"
LABEL Description="Ubuntu 22.04 image with curl and pytest, prepared for the configuration-manager exercise."

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates \
        git && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["/bin/bash"]