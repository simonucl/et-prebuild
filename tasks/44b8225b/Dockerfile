FROM ubuntu:22.04

# Author Maintainer

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash -u 1000 user && \
    chown -R user:user /home/user && \
    mkdir -p /var/spool/cron/crontabs && \
    chmod 1730 /var/spool/cron/crontabs && \
    chown root:crontab /var/spool/cron/crontabs && \
    touch /var/spool/cron/crontabs/user && \
    chmod 600 /var/spool/cron/crontabs/user && \
    chown user:crontab /var/spool/cron/crontabs/user && \
    chmod 755 /home/user

ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH

# Runscript equivalent
CMD ["/bin/bash"]