FROM ubuntu:22.04

# Author="Apptainer Task Prep"
# Description="Environment prepared for dummy restore drill with pytest pre-installed."

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/restore_test && \
    rm -f /home/user/restore_test/restore_session.log && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/restore_test && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# From %environment (commands must be RUN, exports become ENV)
RUN chmod 755 /home/user
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

LABEL Author="Apptainer Task Prep" \
      Description="Environment prepared for dummy restore drill with pytest pre-installed."