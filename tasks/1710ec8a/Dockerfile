FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        jq \
        tar \
        gzip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN printf 'Alpha\n' > /home/user/data/file_a.txt

RUN printf 'Beta\n' > /home/user/data/file_b.txt

RUN chmod -R a+rwX /home/user

LABEL Author="backup-training-setup"

# Container image that provides the initial state for the backup-automation exercise:
# - /home/user/data/file_a.txt   (contains "Alpha\n")
# - /home/user/data/file_b.txt   (contains "Beta\n")
# No /home/user/backups directory is present; the student’s script will create it.
# Pytest is pre-installed for the automated checks.