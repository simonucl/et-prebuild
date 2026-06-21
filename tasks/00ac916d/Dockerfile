FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g user user && \
    mkdir -p /home/user/app/logs && \
    chown -R user:user /home/user && \
    truncate -s 2048 /home/user/app/logs/error.log && \
    truncate -s 3072 /home/user/app/logs/access.log && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/app && \
    chmod 0755 /home/user/app/logs && \
    chmod 0644 /home/user/app/logs/error.log && \
    chmod 0644 /home/user/app/logs/access.log

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Container for the 'log-directory size' exercise.
# Switch to the 'user' account with:   su - user
# Then follow the task instructions.