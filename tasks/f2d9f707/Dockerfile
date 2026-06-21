FROM ubuntu:22.04

# Update package lists and install required packages
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        tzdata && \
    locale-gen de_DE.UTF-8 && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# Persist default environment variables for interactive shells
RUN echo 'export TZ="Europe/Berlin"' > /etc/profile.d/00-time-locale.sh && \
    echo 'export LANG="de_DE.UTF-8"' >> /etc/profile.d/00-time-locale.sh && \
    chmod 0644 /etc/profile.d/00-time-locale.sh

# Set environment variables
ENV TZ="Europe/Berlin"
ENV LANG="de_DE.UTF-8"

# Set home directory permissions
RUN chmod 755 /home/user

# Default action: start an interactive shell
CMD ["/bin/bash"]