FROM ubuntu:22.04

# This container supplies the initial, pristine environment for the
# cron-file creation exercise. It purposely does NOT include any of
# the artefacts that the learner must create (/home/user/cron, the
# *.cron file, or the status log). Pytest is installed so the grading
# infrastructure can run its checks.

LABEL Author="Apptainer Exercise Builder"
LABEL Description="Base image for cron-file creation exercise. Contains Python3 and pytest."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*