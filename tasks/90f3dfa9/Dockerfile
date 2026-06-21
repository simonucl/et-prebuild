FROM ubuntu:22.04

# Converted from %post
RUN set -e && apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip cron
RUN pip3 install --no-cache-dir pytest
RUN mkdir -p /home/user && chmod 0777 /home/user
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# From %labels (chmod must be executed, the rest are actual labels)
RUN chmod 755 /home/user
LABEL Author="Apptainer Build System"
LABEL Description="Base image for credential-rotation exercise; includes Python, pytest, and cron."

# From %environment
ENV PATH="/usr/local/bin:${PATH}"