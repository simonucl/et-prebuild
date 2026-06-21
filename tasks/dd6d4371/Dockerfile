FROM ubuntu:22.04

# Labels
LABEL Author="user_setup_bot"
LABEL Description="Container with pre-populated web access logs for the traffic snapshot exercise. Pytest is installed."

# Help information as comments
# This container image sets up the following starting state for the assignment:
#
#   • /home/user/project/logs/ holds exactly two access log files (each 10 lines).
#   • /home/user/project/reports/ intentionally does NOT exist yet.
#   • pytest is pre-installed so that automated grading can run inside the container.
#
# Students are expected to create the reports directory and generate the required
# report files according to the problem specification.

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user that the outer runtime user can map to
RUN set -e && \
    USERNAME="user" && \
    USER_UID=1000 && \
    USER_GID=1000 && \
    if ! getent group "${USER_GID}" >/dev/null 2>&1; then \
        groupadd -g "${USER_GID}" "${USERNAME}"; \
    fi && \
    if ! getent passwd "${USER_UID}" >/dev/null 2>&1; then \
        useradd -m -u "${USER_UID}" -g "${USER_GID}" -s /bin/bash "${USERNAME}"; \
    fi

# Create project directory structure
RUN mkdir -p /home/user/project/logs

# Create access1.log
RUN cat > /home/user/project/logs/access1.log <<'EOF'
192.168.0.1 - - [10/Jun/2023:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.0.2 - - [10/Jun/2023:10:15:35 +0000] "POST /login HTTP/1.1" 302 512
192.168.0.1 - - [10/Jun/2023:10:15:38 +0000] "GET /style.css HTTP/1.1" 200 2048
10.0.0.5 - - [10/Jun/2023:10:15:40 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.0.1 - - [10/Jun/2023:10:15:42 +0000] "GET /script.js HTTP/1.1" 200 4096
172.16.0.3 - - [10/Jun/2023:10:15:45 +0000] "GET /about HTTP/1.1" 200 512
192.168.0.2 - - [10/Jun/2023:10:15:48 +0000] "GET /dashboard HTTP/1.1" 200 1024
192.168.0.2 - - [10/Jun/2023:10:15:50 +0000] "GET /api/data HTTP/1.1" 200 256
10.0.0.5 - - [10/Jun/2023:10:15:52 +0000] "GET /style.css HTTP/1.1" 200 2048
10.0.0.5 - - [10/Jun/2023:10:15:55 +0000] "GET /script.js HTTP/1.1" 200 4096
EOF

# Create access2.log
RUN cat > /home/user/project/logs/access2.log <<'EOF'
172.16.0.3 - - [11/Jun/2023:11:10:12 +0000] "GET /index.html HTTP/1.1" 200 1024
192.168.0.1 - - [11/Jun/2023:11:10:14 +0000] "GET /contact HTTP/1.1" 200 512
192.168.0.2 - - [11/Jun/2023:11:10:16 +0000] "GET /products HTTP/1.1" 200 2048
192.168.0.2 - - [11/Jun/2023:11:10:18 +0000] "GET /products HTTP/1.1" 200 2048
10.0.0.5 - - [11/Jun/2023:11:10:20 +0000] "GET /checkout HTTP/1.1" 200 1024
172.16.0.3 - - [11/Jun/2023:11:10:22 +0000] "GET /cart HTTP/1.1" 200 512
172.16.0.3 - - [11/Jun/2023:11:10:24 +0000] "GET /cart HTTP/1.1" 200 512
10.0.0.5 - - [11/Jun/2023:11:10:26 +0000] "GET /api/data HTTP/1.1" 200 256
10.0.0.5 - - [11/Jun/2023:11:10:28 +0000] "POST /api/checkout HTTP/1.1" 200 512
10.0.0.5 - - [11/Jun/2023:11:10:30 +0000] "GET /thankyou HTTP/1.1" 200 1024
EOF

# Set ownership and permissions
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod -R a+rX /home/user/project

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user