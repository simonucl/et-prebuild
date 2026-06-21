FROM ubuntu:22.04

# Refresh APT metadata and install required packages
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sysbench \
        fio \
        stress-ng \
        ca-certificates \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Prepare a writable working directory for the learner
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Labels
LABEL Author="benchmark-setup"
LABEL Description="Container for on-call performance benchmark task with pytest pre-installed."

WORKDIR /home/user

CMD ["bash", "-c", "echo 'This container is prepared for the performance-benchmark exercise.' && echo 'Invoke your own scripts/tests after entering the shell.'"]