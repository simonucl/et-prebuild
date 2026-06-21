FROM ubuntu:22.04

# Help / labels
LABEL Author="diagnostics-setup"
LABEL Description="Environment prepared for AcmeWeb diagnostic exercise."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /home/user/app/logs

# access.log
RUN cat <<'EOF' > /home/user/app/logs/access.log
127.0.0.1 - - [15/Sep/2023:14:21:43 +0000] "GET /index.html HTTP/1.1" 200 1024
203.0.113.10 - - [15/Sep/2023:14:22:01 +0000] "POST /login HTTP/1.1" 500 7212
198.51.100.77 - - [15/Sep/2023:14:22:05 +0000] "GET /api/data HTTP/1.1" 500 532
203.0.113.10 - - [15/Sep/2023:14:22:08 +0000] "GET /dashboard HTTP/1.1" 200 854
192.0.2.55 - - [15/Sep/2023:14:22:15 +0000] "GET /reports HTTP/1.1" 500 1300
EOF

# error.log
RUN cat <<'EOF' > /home/user/app/logs/error.log
2023-09-15T14:22:01Z ERROR com.acmeweb.auth.LoginController - NullPointerException
java.lang.NullPointerException
    at com.acmeweb.auth.LoginController.authenticate(LoginController.java:42)
2023-09-15T14:22:05Z ERROR com.acmeweb.api.DataController - IllegalStateException
java.lang.IllegalStateException
    at com.acmeweb.api.DataController.fetch(DataController.java:37)
2023-09-15T14:22:15Z ERROR com.acmeweb.reports.ReportsController - SQLException
java.sql.SQLException
    at com.acmeweb.reports.ReportsController.buildReport(ReportsController.java:55)
2023-09-15T14:23:00Z INFO  HealthCheck - OK
EOF

# Permissions
RUN chmod -R 0755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"