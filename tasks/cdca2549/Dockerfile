FROM ubuntu:22.04

# Labels
LABEL Maintainer="Generated for Apptainer task setup"
LABEL Description="Container with initial state for mock-API integrity check exercise"

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state required by the grading tests
# ------------------------------------------------------------------
RUN mkdir -p /home/user

# 1. /home/user/api_response.txt — exactly 5 bytes: 'hello' (no newline)
RUN printf 'hello' > /home/user/api_response.txt

# 2. /home/user/reference.sha256 — classic sha256sum format, trailing newline
RUN printf '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824  api_response.txt\n' \
    > /home/user/reference.sha256

# Permissions: readable by all; parent dir writable so the student can add files
RUN chmod 644 /home/user/api_response.txt /home/user/reference.sha256 && \
    chmod 777 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD ["/bin/bash"]