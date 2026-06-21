# Converted from Apptainer definition
# Help:
# This image contains sample data under /home/user/sample_data and includes pytest.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        procps \
        tar \
        gzip \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/sample_data

RUN printf 'alpha\n' > /home/user/sample_data/file_alpha.txt && \
    printf 'beta\n'  > /home/user/sample_data/file_beta.txt

RUN chmod 755 /home /home/user /home/user/sample_data && \
    chmod 644 /home/user/sample_data/file_alpha.txt /home/user/sample_data/file_beta.txt

LABEL Author="backup-operator-example"
LABEL Description="Container image pre-populated with sample data for backup/restore task"

# Original runscript (informational only):
# chmod 755 /home/user
# echo "This container is intended for automated testing. Execute your shell commands inside an interactive shell:"
# echo "    apptainer shell <container>"
# Then follow the instructions in the task description.