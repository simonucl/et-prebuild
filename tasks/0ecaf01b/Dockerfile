FROM ubuntu:22.04

# Help:
# This container image provides the initial environment for the log-analysis
# task. Two input log files are pre-populated under /home/user/logs/, and
# pytest is installed so that the provided test suite can validate the
# student’s solution. The /home/user/analysis directory is writable, ready
# for the student to create their reports.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/analysis && \
    chmod 0777 /home/user/analysis

RUN cat <<'EOF' > /home/user/logs/syslog
Jan 12 10:15:23 host sshd[1024]: ERROR Failed password for invalid user admin from 192.168.1.10 port 52222 ssh2
Jan 12 10:16:45 host sshd[1026]: WARNING Authentication delayed for 192.168.1.11 port 52223
Jan 12 10:17:01 host apache2[2048]: ERROR mod_proxy: connect to backend failed
Jan 12 10:17:05 host apache2[2048]: WARNING mod_proxy: retrying request to backend
Jan 12 10:17:10 host sshd[1029]: ERROR Failed password for invalid user root from 192.168.1.12 port 52224 ssh2
Jan 12 10:18:20 host cron[3072]: WARNING Some cron job used deprecated feature
Jan 12 10:19:30 host sshd[1031]: WARNING Connection closed by 192.168.1.11 port 52223 [preauth]
Jan 12 10:20:31 host apache2[2050]: ERROR File does not exist: /var/www/favicon.ico
Jan 12 10:21:40 host apache2[2050]: ERROR client denied by server configuration: /var/www/secret
Jan 12 10:22:45 host sshd[1033]: ERROR Failed password for invalid user admin from 192.168.1.13 port 52226 ssh2
EOF

RUN cat <<'EOF' > /home/user/logs/access.log
192.168.1.10 - - [12/Jan/2023:10:15:23 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.11 - - [12/Jan/2023:10:15:25 +0000] "GET /contact.html HTTP/1.1" 200 512
10.0.0.5      - - [12/Jan/2023:10:15:27 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.12 - - [12/Jan/2023:10:15:29 +0000] "GET /about.html HTTP/1.1" 200 2048
192.168.1.10 - - [12/Jan/2023:10:15:33 +0000] "POST /login HTTP/1.1" 302 128
172.16.0.2   - - [12/Jan/2023:10:15:35 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.10 - - [12/Jan/2023:10:15:37 +0000] "GET /dashboard HTTP/1.1" 200 4096
192.168.1.11 - - [12/Jan/2023:10:15:39 +0000] "GET /pricing HTTP/1.1" 200 2048
192.168.1.10 - - [12/Jan/2023:10:15:41 +0000] "GET /reports HTTP/1.1" 200 2048
203.0.113.8  - - [12/Jan/2023:10:15:43 +0000] "GET /index.html HTTP/1.1" 404 256
10.0.0.5      - - [12/Jan/2023:10:15:45 +0000] "GET /docs HTTP/1.1" 200 1024
192.168.1.11 - - [12/Jan/2023:10:15:47 +0000] "POST /login HTTP/1.1" 302 128
192.168.1.10 - - [12/Jan/2023:10:15:49 +0000] "GET /settings HTTP/1.1" 200 2048
10.0.0.5      - - [12/Jan/2023:10:15:51 +0000] "GET /admin HTTP/1.1" 403 512
192.168.1.11 - - [12/Jan/2023:10:15:53 +0000] "GET /logout HTTP/1.1" 200 256
192.168.1.12 - - [12/Jan/2023:10:15:55 +0000] "GET /reports HTTP/1.1" 200 2048
172.16.0.2   - - [12/Jan/2023:10:15:57 +0000] "GET /faq HTTP/1.1" 200 1024
192.168.1.12 - - [12/Jan/2023:10:15:59 +0000] "GET /dashboard HTTP/1.1" 200 4096
EOF

RUN chmod -R a+r /home/user/logs

RUN chmod 755 /home/user

LABEL Author="Log-Analysis-Task-Setup"