FROM ubuntu:22.04

# Labels
LABEL Author="Exercise Preparation Script"
LABEL Description="Environment for the backup_checks ping exercise with pytest installed."

# Help/Description as comments:
# This container provides the clean starting environment for the
# "backup_checks" ping exercise.  Only /home/user exists; the
# backup_checks directory and loopback_ping.log are intentionally
# absent so the learner can create them.  pytest is installed for the
# verification suite.

RUN set -eux && \
    # Update package lists and install required packages
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        ca-certificates \
        build-essential && \
    # Install pytest for the exercise framework
    pip3 install --no-cache-dir pytest && \
    # Create the expected /home/user directory (writable for any UID)
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up APT caches to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Minimal PATH setup
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /home/user