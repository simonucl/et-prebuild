FROM ubuntu:22.04

# Author="Container preparer – tasks@platform"
# Description="Initial state for INI audit scripting task"

ENV PATH="/home/user/bin:$PATH"
ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

RUN mkdir -p /home/user/configs /home/user/bin /home/user/reports && \
    chmod -R 777 /home/user

RUN cat <<'EOF' > /home/user/configs/appA.ini
[meta]
name = Application Alpha
version = 1.2.3

[cpu]
threshold = 75
limit = 90

[memory]
threshold = 1024
limit = 2048

[io]
threshold = 120
limit = 150
EOF

RUN cat <<'EOF' > /home/user/configs/appB.ini
[meta]
name = Beta Service
version = 4.5.6

[cpu]
threshold = 85
limit = 80

[memory]
threshold = 1500
limit = 1400

[io]
threshold = 100
limit = 200
EOF

RUN chmod 644 /home/user/configs/appA.ini /home/user/configs/appB.ini && \
    chmod 755 /home/user