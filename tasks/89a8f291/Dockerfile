FROM ubuntu:22.04

# Help / description
# Container for the legacy config encoding exercise.
# Author: legacy-config-exercise
# Description: Environment for the legacy config encoding conversion task

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        file \
        locales && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/cicd

RUN cat <<'EOF' | iconv -f UTF-8 -t windows-1252 > /home/user/projects/cicd/legacy_config_win1252.txt
# Build configuration – ACME CI/CD
BUILD_SERVER=alpha
DEPLOY_TARGET=production
CURRENCY=€
EOF

RUN chmod -R a+rX /home/user

LABEL Author="legacy-config-exercise"
LABEL Description="Environment for the legacy config encoding conversion task"

CMD /bin/sh -c "echo 'Container for the legacy config encoding exercise.' && echo 'Switch to /home/user/projects/cicd and begin your work.' && exec \"$@\""