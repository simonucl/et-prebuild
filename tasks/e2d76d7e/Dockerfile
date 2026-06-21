FROM ubuntu:22.04

# Ensure non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial project structure under /home/user
RUN mkdir -p /home/user/api-test/config && \
    mkdir -p /home/user/api-test/logs && \
    mkdir -p /home/user/backup

# Project files
RUN printf 'API Test Project\n' > /home/user/api-test/README.md && \
    printf 'endpoint: "https://example.com/api"\nretries: 3\n' \
        > /home/user/api-test/config/config.yaml && \
    printf '{"status":"ok","date":"2023-09-15"}\n' \
        > /home/user/api-test/logs/2023-09-15_01.json && \
    printf '{"status":"ok","date":"2023-09-16"}\n' \
        > /home/user/api-test/logs/2023-09-16_01.json && \
    printf '{"status":"ok","date":"2023-09-17"}\n' \
        > /home/user/api-test/logs/2023-09-17_01.json

# Permissions: everything readable; backup dir writable for any user
RUN chmod -R a+rX /home/user/api-test && \
    chmod 0777 /home/user/backup && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1