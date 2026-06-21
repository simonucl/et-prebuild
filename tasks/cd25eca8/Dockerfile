FROM ubuntu:22.04

# Author: Automated Build
# Description: Base image for the "compliance" task – includes Python, PyPI,
#              pytest, and a writable /home/user directory, but **does not**
#              create any of the artefacts the student must produce later.

# Help:
# This image supplies:
#   • Python 3 and pip
#   • pytest (required by the grading harness)
#   • A writable /home/user directory
# It deliberately does NOT create any of the compliance-exercise artefacts
# (directory, script, logs, summary file). Those must be produced by the
# learner during the assessment.

RUN set -e && \
    # Refresh package index and install Python tooling
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools \
        locales \
        ca-certificates && \
    # Ensure utf-8 locale is available
    locale-gen en_US.UTF-8 && \
    # Install pytest for the grading harness
    pip3 install --no-cache-dir pytest && \
    # Prepare a writable /home/user directory.
    # (DO NOT create the /home/user/compliance structure – that is the
    # student's responsibility and the tests ensure it does not yet exist.)
    mkdir -p /home/user && \
    # Make it easy for whatever (non-root) UID runs inside the container to
    # write into /home/user.
    chmod 0777 /home/user && \
    # Provide a convenient python alias
    ln -s /usr/bin/python3 /usr/local/bin/python || true && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/user/.local/bin:${PATH}"

WORKDIR /home/user

CMD ["/bin/bash"]