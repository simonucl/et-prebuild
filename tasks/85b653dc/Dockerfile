FROM ubuntu:22.04

# Labels
LABEL Author="Exercise Preparation Bot"
LABEL Description="Container for timezone conversion task; includes Python and pytest, plus a clean /home/user workspace."

# Post section
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata \
        ca-certificates && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment section
RUN chmod 755 /home/user
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin