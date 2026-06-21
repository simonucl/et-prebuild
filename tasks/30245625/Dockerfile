FROM ubuntu:22.04

# Labels
LABEL Author="SingularityGPT"
LABEL Description="Container prepared for the \"fixed time-zone and locale\" exercise. Provides Python, pytest, and a default /home/user with a basic .bashrc."

# Base utilities and Python tooling
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8

# Prepare non-privileged working environment: /home/user
RUN set -e && \
    user_home="/home/user" && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d "$user_home" -s /bin/bash user; \
    else \
        mkdir -p "$user_home"; \
    fi && \
    if [ -f /etc/skel/.bashrc ]; then \
        cp /etc/skel/.bashrc "$user_home/.bashrc"; \
    else \
        touch "$user_home/.bashrc"; \
    fi && \
    chown -R user:user "$user_home" && \
    chmod 755 "$user_home"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default entry point: open an interactive shell
CMD ["/bin/bash"]