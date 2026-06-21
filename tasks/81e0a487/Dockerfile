FROM ubuntu:22.04

# Help text
# This container image provides the initial state for the
# “backup-operator test restore” task. Three source data files are
# placed under /home/user/data. No backup_logs or restored_data
# directories exist yet. Pytest is installed system-wide so that the
# grading harness can verify the environment and results.

LABEL Author="Apptainer Automation"
LABEL Description="Environment for backup / restore verification exercise with pytest pre-installed."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/data && \
    chmod 0755 /home/user/data && \
    printf 'Alpha backup test file.\n' > /home/user/data/file1.txt && \
    printf 'Bravo second file line 1.\nBravo line 2.\n' > /home/user/data/file2.txt && \
    printf 'Charlie 3rd file\nlineB\n' > /home/user/data/file3.txt && \
    chmod 0644 /home/user/data/file1.txt /home/user/data/file2.txt /home/user/data/file3.txt && \
    rm -rf /home/user/backup_logs /home/user/restored_data

# From %environment
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8