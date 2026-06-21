FROM ubuntu:22.04

# Baseline environment with curl and pytest for the health-check assignment.
# Author: health-check-template

RUN set -e && apt-get update

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-pip

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="health-check-template"
LABEL Description="Baseline environment with curl and pytest for the health-check assignment."