FROM ubuntu:22.04

# Author example
# Description Initial state for artifact-curation exercise (with pytest pre-installed)
# Help:
# This container prepares the starting environment for the “artifact curation”
# exercise. It installs pytest and seeds /home/user/downloads with the three
# placeholder binaries that the learner is expected to manage.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/downloads && \
    printf "alpha-1.0 binary\n"   > /home/user/downloads/alpha-1.0.jar && \
    printf "bravo-2.1 package\n"  > /home/user/downloads/bravo-2.1.rpm && \
    printf "charlie-3.4 package\n" > /home/user/downloads/charlie-3.4.deb && \
    touch /home/user/.bashrc && \
    chmod -R 0777 /home/user

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin