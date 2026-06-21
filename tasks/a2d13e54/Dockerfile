FROM ubuntu:22.04

# Help
# This Apptainer container provides the initial filesystem state and all
# dependencies (Python + pytest) required for the “backup administrator”
# coding exercise.

LABEL Author="Unknown"
LABEL Description="Environment for CSV→JSON archiving task with pytest pre-installed."

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8

RUN mkdir -p /home/user/backups

RUN cat > /home/user/backups/servers_2023-10-15.csv <<'CSVEOF'
id,hostname,ip
1,web01,192.168.1.10
2,db01,192.168.1.20
CSVEOF

RUN mkdir -p /home/user/backups/archive && \
    : > /home/user/backups/archive/archive.log

RUN chmod -R a+rwX /home/user && chmod 755 /home/user