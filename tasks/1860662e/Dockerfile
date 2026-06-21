FROM ubuntu:22.04

# Labels
LABEL Author="exercise-prep-bot"
LABEL Description="Environment for timezone conversion exercise"

# Install essentials
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        locales \
        tzdata && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Set working directory
WORKDIR /home/user

# Help information (as comments):
# This container provides a clean environment for the timezone conversion
# exercise.  It supplies:
#   • /home/user directory (initially empty)
#   • Locale en_US.UTF-8
#   • tzdata for timezone computations
#   • pytest for the assessment harness