# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %help
# This container image sets up the initial state for the provisioning-summary
# task. It ships:
#   • a non-privileged user: user
#   • the instance_requests.log file in /home/user/provisioning
#   • pytest pre-installed for the validation suite
# The /home/user/provisioning/report directory is intentionally absent; the
# student’s solution must create it along with the required output file.

LABEL Author="someone@example.com"
LABEL Description="Environment for EC2 instance-type frequency summarisation exercise"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    install -d -o user -g user /home/user/provisioning && \
    rm -rf /home/user/provisioning/report || true

RUN cat <<'EOF' > /home/user/provisioning/instance_requests.log
t2.micro
m5.large
t2.micro
c5.xlarge
t2.micro
m5.large
c5.large
EOF

RUN chown user:user /home/user/provisioning/instance_requests.log

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

WORKDIR /home/user

CMD ["/bin/bash"]