# Author: Your Name
# Description: Environment for the compliance rsync exercise with pytest pre-installed.
# This container provides the starting filesystem state and the tools
# (rsync, Python, pytest) necessary for completing the compliance-report
# synchronisation task.

FROM ubuntu:22.04

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    mkdir -p /home/user/compliance_reports && \
    chmod 755 /home/user/compliance_reports && \
    printf 'Quarter 1 compliance results – draft\n' > /home/user/compliance_reports/report_Q1.txt && \
    printf 'Quarter 2 compliance results – draft\n' > /home/user/compliance_reports/report_Q2.txt && \
    chmod 644 /home/user/compliance_reports/report_Q1.txt && \
    chmod 644 /home/user/compliance_reports/report_Q2.txt && \
    mkdir -p /home/user/remote_mount/compliance_staging && \
    chmod 755 /home/user/remote_mount && \
    chmod 755 /home/user/remote_mount/compliance_staging && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*