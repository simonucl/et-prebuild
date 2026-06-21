# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container image contains:
#   • Three legacy INI configuration files in /home/user/data/configs
#   • Python 3 and pytest pre-installed
# The runtime user can create /home/user/analysis and required output artefacts there.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data/configs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data && \
    chmod 0777 /home/user/data/configs

RUN cat > /home/user/data/configs/app1.ini << 'EOF'
[general]
name = Alpha
version = 1.2.0

[network]
port = 8080
host = 127.0.0.1

[thresholds]
cpu = 85
memory = 65
disk = 90

EOF

RUN cat > /home/user/data/configs/app2.ini << 'EOF'
[general]
name = Beta
version = 2.4.1

[network]
port = 9090
host = 192.168.1.10

[thresholds]
cpu = 50
memory = 75
disk = 60

EOF

RUN cat > /home/user/data/configs/app3.ini << 'EOF'
[general]
name = Gamma
version = 3.1.5

[network]
port = 7070
host = 10.0.0.5

[thresholds]
cpu = 95
memory = 80
disk = 70
temperature = 88

EOF

RUN chmod -R a+r /home/user/data/configs && chmod 755 /home/user

# Labels
LABEL Author="Container build script"
LABEL Description="Provides the pristine environment (legacy INI files + pytest) for the threshold auditing task."