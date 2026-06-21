FROM ubuntu:22.04

# Help text from Apptainer %help section
# This container provides the starter filesystem layout for the
# “one-touch” compliance audit assignment. It includes:
#   • /home/user/compliance_audit/sample_data/ with two predefined files
#   • GNU make and standard POSIX utilities
#   • Python 3 and pytest for automated grading
# Students are expected to supply a Makefile and generated artefacts;
# none are present in the image.

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    echo "Updating apt repositories and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-pip \
        ca-certificates \
        findutils \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest (system-wide)..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating user 'user' and workspace directories..." && \
    useradd -m -s /bin/bash user && \
    mkdir -p /home/user/compliance_audit/sample_data && \
    touch /home/user/compliance_audit/sample_data/file1.txt && \
    printf 'abc' > /home/user/compliance_audit/sample_data/file2.txt && \
    chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/compliance_audit /home/user/compliance_audit/sample_data && \
    chmod 644 /home/user/compliance_audit/sample_data/file1.txt /home/user/compliance_audit/sample_data/file2.txt

LABEL Author="Automated build for compliance_audit starter environment"
LABEL Version="1.0"