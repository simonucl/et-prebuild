FROM ubuntu:22.04

# Labels
LABEL Author="timezone_debug_setup"
LABEL Description="Base image for the timezone_debug exercise – contains Python, pytest and a writable /home/user."

# Update apt cache and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        locales \
        tzdata \
        ca-certificates && \
    # Ensure UTF-8 locale is generated (needed by many tools)
    sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    # Install pytest for the grading suite
    pip3 install --no-cache-dir pytest && \
    # Prepare a writable home directory expected by the tests
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV HOME=/home/user

WORKDIR /home/user

CMD ["echo", "Container for the timezone_debug exercise. Use 'docker exec' or 'docker run -it' to work inside."]