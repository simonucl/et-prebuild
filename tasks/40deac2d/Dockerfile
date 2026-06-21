FROM ubuntu:22.04

# Help section was not provided in the original file

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backup_demo/original

RUN printf 'hello' > /home/user/backup_demo/original/sample.txt

RUN chmod -R 0777 /home/user

# From %environment
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH