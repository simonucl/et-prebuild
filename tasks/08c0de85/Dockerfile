FROM ubuntu:22.04

# Author: Singularity-Prep
# Description: Initial state for compliance CSV merging task: raw data present, pytest installed.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/raw

RUN cat >/home/user/raw/hostnames.csv <<'EOF'
HOSTNAME
server01
server02
db01
web02
proxy01
EOF

RUN cat >/home/user/raw/os.csv <<'EOF'
OS
Ubuntu 20.04
CentOS 8
Ubuntu 18.04
Debian 10
AlmaLinux 9
EOF

RUN cat >/home/user/raw/patch_status.csv <<'EOF'
PATCH_STATUS
Compliant
Non-Compliant
Compliant
Compliant
Non-Compliant
EOF

RUN cat >/home/user/raw/av_status.csv <<'EOF'
AV_STATUS
Enabled
Disabled
Enabled
Enabled
Disabled
EOF

RUN chmod 755 /home/user /home/user/raw && \
    chmod 644 /home/user/raw/*.csv