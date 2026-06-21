FROM ubuntu:22.04

# Help section (none provided)

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        locales \
        ca-certificates && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/devsecops-policy && \
    echo "requests==2.31.0" > /home/user/devsecops-policy/allowed_packages.txt && \
    chmod -R a+rwX /home/user/devsecops-policy && \
    chmod 755 /home/user

# Environment section
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8