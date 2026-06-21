FROM ubuntu:22.04

LABEL Author="AutomatedSetup"
LABEL Description="Environment for artifact-tracking task with initial experiment data."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/experiments/exp_alpha && \
    mkdir -p /home/user/experiments/exp_beta

# exp_alpha → 19 bytes
RUN printf 'dummy model alpha \n' > /home/user/experiments/exp_alpha/model_alpha.pkl

# exp_beta  → 34 bytes
RUN printf 'dummy model beta with bigger size\n' > /home/user/experiments/exp_beta/model_beta.pkl

# Ensure the non-root runtime user can write into /home/user
RUN chmod -R a+rwX /home/user

WORKDIR /home/user

ENTRYPOINT ["sh", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]