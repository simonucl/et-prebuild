FROM ubuntu:22.04

# Help text
# Container prepared for the “build-report” assignment.
# - Pre-populated /home/user/builds with exact files & sizes.
# - pytest installed for automated grading.

ENV PATH=/usr/local/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/builds/projectA && \
    mkdir -p /home/user/builds/projectB && \
    mkdir -p /home/user/builds/projectC && \
    mkdir -p /home/user/builds/old/projectX

RUN truncate -s 12582912 /home/user/builds/projectA/artifact-1.0.0.tar.gz && \
    truncate -s 70        /home/user/builds/projectA/artifact-1.0.0.sha256 && \
    truncate -s 26214400 /home/user/builds/projectB/artifact-2.1.3.tar.gz && \
    truncate -s 3145728  /home/user/builds/projectB/artifact-2.1.3.doc.pdf && \
    truncate -s 8388608  /home/user/builds/projectC/artifact-3.4.5.tar.gz && \
    truncate -s 41943040 /home/user/builds/old/projectX/artifact-0.9.9.tar.gz && \
    truncate -s 1536     /home/user/builds/README.txt

RUN chmod -R a+rX /home/user && \
    chmod 755 /home/user