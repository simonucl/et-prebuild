FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Base image for QA test-environment automation task – provides pytest and required writable directories."

# Help information (as comments)
# This container supplies the initial filesystem state expected by the
# automated grading suite.  Key points:
#   • /home/user/scripts exists and is writable/executable.
#   • /home/user/test_envs exists and is writable (though the assignment
#     allows for its absence; we provide it for convenience).
#   • pytest is installed for the grader.

RUN set -e && \
    echo "Updating APT and installing prerequisites..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash \
        git \
        wget && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating required directory structure with permissive permissions ..." && \
    mkdir -p /home/user && \
    mkdir -p /home/user/scripts && \
    mkdir -p /home/user/test_envs && \
    chmod 0777 /home && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/scripts && \
    chmod 0777 /home/user/test_envs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /home/user