FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Python tooling required for the grading harness
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the tests
RUN mkdir -p /home/user/project/config

RUN printf 'project_name=AwesomeApp\r\nversion=1.2.3\r\nmaintainer=DevOps Team\r\n' \
    > /home/user/project/config/build.cfg

RUN printf 'deploy_env=production\r\nservers=5\r\nstrategy=rolling\r\n' \
    > /home/user/project/config/deploy.cfg

RUN printf 'tests_enabled=true\r\ntimeout=300\r\nretries=2\r\n' \
    > /home/user/project/config/test.cfg

# Permissions – allow non-root container users to read/write/execute
RUN chmod 777 /home/user /home/user/project /home/user/project/config && \
    chmod 666 /home/user/project/config/*.cfg

LABEL Author="encoding-conversion-task-preparer"