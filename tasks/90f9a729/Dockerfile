FROM ubuntu:22.04

# Help / labels
# Author: container-build-script
# Description: Ubuntu 22.04 image prepared for capacity planner assignment with pytest installed.
LABEL Author="container-build-script" \
      Description="Ubuntu 22.04 image prepared for capacity planner assignment with pytest installed."

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    if ! grep -qE '^user:' /etc/passwd; then \
        echo 'user:x:1000:1000::/home/user:/bin/bash' >> /etc/passwd; \
        echo 'user:x:1000:' >> /etc/group; \
    fi && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

CMD ["/bin/bash"]