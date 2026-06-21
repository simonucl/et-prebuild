# Author ChatGPT
# Description "Container with pre-populated nmap scan logs for parsing task"
# This container provides three pre-populated nmap scan log files in
# /home/user/scan_logs for the parsing & benchmarking assignment. Pytest is
# installed so that the grading harness can run its tests.

FROM ubuntu:22.04

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        ca-certificates

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/scan_logs

RUN cat > /home/user/scan_logs/scan1.log <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-24 12:00 CET
Nmap scan report for 10.0.0.5
Host is up (0.00029s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https

Nmap done: 1 IP address (1 host up) scanned in 0.36 seconds
#METRIC real 0m0.362s user 0m0.026s sys 0m0.004s
EOF

RUN cat > /home/user/scan_logs/scan2.log <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-24 12:02 CET
Nmap scan report for 10.0.0.12
Host is up (0.00041s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
25/tcp   open  smtp

Nmap done: 1 IP address (1 host up) scanned in 0.42 seconds
#METRIC real 0m0.428s user 0m0.030s sys 0m0.005s
EOF

RUN cat > /home/user/scan_logs/scan3.log <<'EOF'
Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-24 12:05 CET
Nmap scan report for 10.0.0.20
Host is up (0.00057s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
25/tcp   open  smtp
993/tcp  open  imaps
995/tcp  open  pop3s

Nmap done: 1 IP address (1 host up) scanned in 0.67 seconds
#METRIC real 0m0.672s user 0m0.033s sys 0m0.006s
EOF

RUN chmod 1777 /home/user && \
    chmod 755 /home/user/scan_logs && \
    chmod 644 /home/user/scan_logs/*.log