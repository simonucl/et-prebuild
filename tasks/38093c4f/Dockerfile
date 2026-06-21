FROM ubuntu:22.04

# Author AI-Prep
# Description "Environment for the release-audit task with pre-populated releases and pytest installed."

RUN set -e && \
    echo "Updating package lists and installing required packages..." && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating base directory layout under /home/user ..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/releases

RUN set -e && \
    echo "Populating release directories with exact-sized files..." && \
    mkdir -p /home/user/releases/app_v1.0 /home/user/releases/app_v1.0/bin && \
    truncate -s 512 /home/user/releases/app_v1.0/README.txt && chmod 0644 /home/user/releases/app_v1.0/README.txt && \
    truncate -s 1536 /home/user/releases/app_v1.0/bin/app.bin && chmod 0644 /home/user/releases/app_v1.0/bin/app.bin && \
    mkdir -p /home/user/releases/app_v1.1 /home/user/releases/app_v1.1/bin /home/user/releases/app_v1.1/docs && \
    truncate -s 1024 /home/user/releases/app_v1.1/README.txt && chmod 0644 /home/user/releases/app_v1.1/README.txt && \
    truncate -s 2048 /home/user/releases/app_v1.1/bin/app.bin && chmod 0644 /home/user/releases/app_v1.1/bin/app.bin && \
    truncate -s 3072 /home/user/releases/app_v1.1/docs/CHANGELOG.md && chmod 0644 /home/user/releases/app_v1.1/docs/CHANGELOG.md && \
    mkdir -p /home/user/releases/app_v2.0 /home/user/releases/app_v2.0/bin /home/user/releases/app_v2.0/scripts && \
    truncate -s 2048 /home/user/releases/app_v2.0/README.txt && chmod 0644 /home/user/releases/app_v2.0/README.txt && \
    truncate -s 3072 /home/user/releases/app_v2.0/bin/app.bin && chmod 0644 /home/user/releases/app_v2.0/bin/app.bin && \
    truncate -s 2048 /home/user/releases/app_v2.0/scripts/migrate.sh && chmod 0644 /home/user/releases/app_v2.0/scripts/migrate.sh && \
    find /home/user/releases -type d -exec chmod 0755 {} \; && \
    echo "Initial state successfully prepared."

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN chmod 755 /home/user

CMD ["/bin/bash"]