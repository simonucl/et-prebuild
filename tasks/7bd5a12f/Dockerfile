FROM ubuntu:22.04

# Help text
# This container provides the initial state and tooling for the
# “storage administrator” task. The learner will enter the container
# and perform the required filesystem operations. pytest is installed
# for automated grading.

ENV PYTHONIOENCODING=UTF8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs/app1 && \
    mkdir -p /home/user/logs/app2 && \
    printf 'Error ABC\n'   > /home/user/logs/app1/log1.txt && \
    printf 'Warning XYZ\n' > /home/user/logs/app1/log2.txt && \
    printf 'Debug 123\n'   > /home/user/logs/app2/logA.txt && \
    chmod -R 777 /home/user

LABEL chmod="755 /home/user"
LABEL Author="example@example.com"
LABEL Description="Starter environment for the storage-administrator symlink exercise"