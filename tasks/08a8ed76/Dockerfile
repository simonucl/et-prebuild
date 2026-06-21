FROM ubuntu:22.04

# From %post
RUN set -e && \
    apt-get -y update && \
    apt-get -y install --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure /home/user exists and fix permissions (from %environment)
RUN mkdir -p /home/user && chmod 755 /home/user

# Startup-time access log preparation (converted from %environment as comments)
# The original Apptainer %environment block contained a shell function that
# executes at container start, which Docker cannot emulate directly.
# Below we recreate the access log at build time instead.

RUN mkdir -p /home/user/logs

RUN cat > /home/user/logs/access.log <<'EOF'
192.168.0.10 - - [12/Mar/2023:10:15:01 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
192.168.0.10 - - [12/Mar/2023:10:15:03 +0000] "GET /old-page.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"
192.168.0.10 - - [12/Mar/2023:10:15:05 +0000] "POST /api/data HTTP/1.1" 200 2048 "-" "curl/7.81.0"
192.168.0.10 - - [12/Mar/2023:10:15:07 +0000] "GET /about.html HTTP/1.1" 200 1536 "-" "Mozilla/5.0"
192.168.0.10 - - [12/Mar/2023:10:15:09 +0000] "POST /process.php HTTP/1.1" 404 256 "-" "curl/7.81.0"
192.168.0.10 - - [12/Mar/2023:10:15:11 +0000] "GET /styles.css HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
192.168.0.10 - - [12/Mar/2023:10:15:13 +0000] "POST /submit-form HTTP/1.1" 200 1024 "-" "curl/7.81.0"
192.168.0.10 - - [12/Mar/2023:10:15:15 +0000] "GET /missing.html HTTP/1.1" 404 256 "-" "Mozilla/5.0"
172.16.0.5 - - [12/Mar/2023:11:20:01 +0000] "GET /home HTTP/1.1" 200 3072 "-" "Mozilla/5.0"
172.16.0.5 - - [12/Mar/2023:11:20:03 +0000] "GET /data HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
172.16.0.5 - - [12/Mar/2023:11:20:05 +0000] "POST /login HTTP/1.1" 200 2048 "-" "curl/7.81.0"
172.16.0.5 - - [12/Mar/2023:11:20:07 +0000] "POST /save HTTP/1.1" 200 1024 "-" "curl/7.81.0"
172.16.0.5 - - [12/Mar/2023:11:20:09 +0000] "POST /login.php HTTP/1.1" 404 128 "-" "curl/7.81.0"
172.16.0.5 - - [12/Mar/2023:11:20:11 +0000] "GET /error HTTP/1.1" 500 512 "-" "Mozilla/5.0"
10.0.0.3 - - [12/Mar/2023:12:05:01 +0000] "GET /dashboard HTTP/1.1" 200 4096 "-" "Mozilla/5.0"
10.0.0.3 - - [12/Mar/2023:12:05:03 +0000] "GET /report HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
10.0.0.3 - - [12/Mar/2023:12:05:05 +0000] "GET /admin.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"
10.0.0.3 - - [12/Mar/2023:12:05:07 +0000] "GET /stats HTTP/1.1" 200 3072 "-" "Mozilla/5.0"
10.0.0.3 - - [12/Mar/2023:12:05:09 +0000] "GET /server-error HTTP/1.1" 500 256 "-" "Mozilla/5.0"
203.0.113.55 - - [12/Mar/2023:13:40:01 +0000] "GET /contact.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"
203.0.113.55 - - [12/Mar/2023:13:40:03 +0000] "GET /shop HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
203.0.113.55 - - [12/Mar/2023:13:40:05 +0000] "GET /product HTTP/1.1" 200 1536 "-" "Mozilla/5.0"
203.0.113.55 - - [12/Mar/2023:13:40:07 +0000] "GET /pricing HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
198.51.100.77 - - [12/Mar/2023:14:10:01 +0000] "POST /signup HTTP/1.1" 200 2048 "-" "curl/7.81.0"
198.51.100.77 - - [12/Mar/2023:14:10:03 +0000] "POST /preferences HTTP/1.1" 200 1024 "-" "curl/7.81.0"
198.51.100.77 - - [12/Mar/2023:14:10:05 +0000] "POST /signup.php HTTP/1.1" 404 128 "-" "curl/7.81.0"
127.0.0.1 - - [12/Mar/2023:14:55:01 +0000] "GET /health HTTP/1.1" 200 64 "-" "curl/7.81.0"
EOF

# From %labels
LABEL Author="task-preparation-bot"
LABEL Description="Sets up the initial environment for the Apache log parsing assignment, including the reference access log and pytest installation."