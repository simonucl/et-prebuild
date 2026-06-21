FROM ubuntu:22.04

# Help section omitted (none provided)

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/tickets/issue_20230815 && \
    mkdir -p /home/user/backups

RUN printf 'User unable to connect to VPN.\n' \
    > /home/user/tickets/issue_20230815/notes.txt

RUN printf '[2023-08-15 10:03] Ping to vpn.company.com failed.\n' \
    > /home/user/tickets/issue_20230815/diagnostics.log

RUN dd if=/dev/urandom of=/home/user/tickets/issue_20230815/screenshot.png \
    bs=10 count=1 status=none

RUN chmod -R a+rX /home/user/tickets && \
    chmod 0777 /home/user/backups && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin