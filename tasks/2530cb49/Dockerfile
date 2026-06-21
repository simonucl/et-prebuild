FROM ubuntu:22.04

# Help: Container ready for the open-ports CSV pipeline exercise.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mock_scans && \
    chmod 755 /home/user /home/user/mock_scans

RUN cat >/home/user/mock_scans/10.0.0.5.nmap <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2023-12-01 10:00 UTC
Nmap scan report for 10.0.0.5
Host is up (0.00020s latency).
Not shown: 997 filtered ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp closed https

Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds
EOF

RUN cat >/home/user/mock_scans/10.0.0.8.nmap <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2023-12-01 10:02 UTC
Nmap scan report for 10.0.0.8
Host is up (0.00025s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
23/tcp  open  telnet
80/tcp  closed http

Nmap done: 1 IP address (1 host up) scanned in 1.05 seconds
EOF

RUN cat >/home/user/mock_scans/10.0.0.12.nmap <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2023-12-01 10:05 UTC
Nmap scan report for 10.0.0.12
Host is up (0.00021s latency).
Not shown: 996 filtered ports
PORT    STATE SERVICE
25/tcp  open  smtp
110/tcp open  pop3
143/tcp open  imap
53/udp  open  domain

Nmap done: 1 IP address (1 host up) scanned in 1.33 seconds
EOF

RUN chmod 644 /home/user/mock_scans/*.nmap