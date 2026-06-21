FROM ubuntu:22.04

# HELP: Container for the “DNS allow-list audit” exercise.
# Includes pytest and pre-creates the initial policy directory with dns_allowlist.txt.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/policy && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/policy && \
    printf 'localhost\ninvalid.local\n' > /home/user/policy/dns_allowlist.txt && \
    chmod 0644 /home/user/policy/dns_allowlist.txt

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="Apptainer task setup"