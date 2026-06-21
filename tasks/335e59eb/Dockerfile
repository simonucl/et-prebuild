# Author: maintenance-task-preparer
# Description: Base image for CI/CD maintenance task – initial workspace state + pytest

FROM ubuntu:22.04

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        tzdata \
        gzip \
        coreutils \
        findutils && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user

RUN install -d -m 0777 /home/user/cicd_workspace/build_logs && \
    install -d -m 0777 /home/user/cicd_workspace/test_results && \
    install -d -m 0777 /home/user/cicd_workspace/artifacts/dist && \
    install -d -m 0755 /home/user/maintenance

RUN dd if=/dev/zero of=/home/user/cicd_workspace/build_logs/build1.log bs=1024 count=1500 status=none && \
    dd if=/dev/zero of=/home/user/cicd_workspace/build_logs/build2.log bs=1024 count=500  status=none && \
    dd if=/dev/zero of=/home/user/cicd_workspace/build_logs/build3.log bs=1024 count=2048 status=none

RUN echo "old build tmp" > /home/user/cicd_workspace/build_logs/old_build.tmp && \
    echo "testrun1 tmp"  > /home/user/cicd_workspace/test_results/testrun1.tmp && \
    echo "testrun2 tmp"  > /home/user/cicd_workspace/test_results/testrun2.tmp && \
    echo "artifact tmp"  > /home/user/cicd_workspace/artifacts/dist/artifact.tmp && \
    chmod -R 0777 /home/user && \
    chmod 755 /home/user

# Help:
# This image provides the initial file-system state and dependencies for the
# CI/CD workspace maintenance task. Pytest is pre-installed so that the task’s
# verification suite can be executed inside the container.

CMD echo "This container is prepared for the CI/CD maintenance task." && exec "$@"