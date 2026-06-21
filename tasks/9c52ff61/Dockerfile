FROM ubuntu:22.04

# System packages and Python tooling
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem and user area
RUN mkdir -p /home/user/server_logs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/server_logs

# access.log
RUN cat > /home/user/server_logs/access.log << 'EOF'
192.168.1.10 - - [12/Oct/2023:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.15 - - [12/Oct/2023:10:17:05 +0000] "POST /login HTTP/1.1" 302 512
192.168.1.10 - - [12/Oct/2023:10:17:20 +0000] "GET /dashboard HTTP/1.1" 200 2048
192.168.1.20 - - [12/Oct/2023:10:18:11 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.15 - - [13/Oct/2023:09:02:17 +0000] "GET /home HTTP/1.1" 200 1500
192.168.1.10 - - [13/Oct/2023:09:05:33 +0000] "GET /settings HTTP/1.1" 200 512
192.168.1.10 - - [13/Oct/2023:09:10:00 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.20 - - [13/Oct/2023:09:12:47 +0000] "GET /dashboard HTTP/1.1" 404 256
192.168.1.15 - - [14/Oct/2023:11:22:10 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.1.25 - - [14/Oct/2023:11:23:40 +0000] "GET /profile HTTP/1.1" 200 768
192.168.1.25 - - [14/Oct/2023:11:24:15 +0000] "GET /profile HTTP/1.1" 200 768
192.168.1.15 - - [14/Oct/2023:11:25:00 +0000] "POST /update HTTP/1.1" 200 256
EOF

# error.log
RUN cat > /home/user/server_logs/error.log << 'EOF'
2023-10-12 10:15:33,451 ERROR Disk full on /dev/sda1
2023-10-12 10:17:06,460 WARNING User admin failed login
2023-10-12 10:18:11,570 ERROR Unable to reach database
2023-10-13 09:02:20,123 INFO System watchdog
2023-10-13 09:05:40,300 ERROR High memory usage detected
2023-10-13 09:10:05,400 ERROR Disk full on /dev/sdb1
2023-10-14 11:22:15,500 ERROR Service httpd crashed
2023-10-14 11:23:50,600 WARNING Low disk space
2023-10-14 11:24:20,700 ERROR Failed to start backup task
2023-10-14 11:25:05,800 INFO Backup task queued
EOF

# usage.csv
RUN cat > /home/user/server_logs/usage.csv << 'EOF'
server,date,cpu_percent,mem_percent
srv1,2023-10-12 10:00,35,60
srv2,2023-10-12 10:00,40,55
srv1,2023-10-12 11:00,45,65
srv2,2023-10-12 11:00,50,60
srv3,2023-10-13 09:00,20,40
srv1,2023-10-13 09:00,30,50
srv2,2023-10-13 09:00,60,70
srv3,2023-10-14 11:00,25,45
srv1,2023-10-14 11:00,40,55
srv2,2023-10-14 11:00,55,65
EOF

RUN chmod 0644 /home/user/server_logs/*.log /home/user/server_logs/*.csv && \
    chmod 755 /home/user

ENV PATH="$PATH:/home/user/.local/bin"