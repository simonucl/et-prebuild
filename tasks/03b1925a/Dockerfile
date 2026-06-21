FROM ubuntu:22.04

# Help / runscript notes
# This container is prepared for the FinOps analyst assignment.
# Invoke your solution script or open a shell to begin.

ENV PYTHONIOENCODING=UTF-8

LABEL Author="FinOps-Setup-Script"
LABEL Description="Environment for FinOps checksum verification assignment"
LABEL Version="1.0"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/cloud_invoices && \
    printf 'abc' > /home/user/cloud_invoices/AWS_2023-07.csv && \
    printf 'hello' > /home/user/cloud_invoices/GCP_2023-07.csv && \
    chmod 755 /home/user && \
    chmod 755 /home/user/cloud_invoices && \
    chmod 644 /home/user/cloud_invoices/AWS_2023-07.csv /home/user/cloud_invoices/GCP_2023-07.csv

CMD ["/bin/bash"]