FROM ubuntu:22.04

# Basic tools and Python + Pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        file \
        locales && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pytest

# Prepare initial directory structure
RUN mkdir -p /home/user/logs

# Create UTF-8 log file
RUN cat > /home/user/logs/session_utf8_temp.log <<'EOF'
2023-05-01 12:00:00 INFO  User São logged in
2023-05-01 12:02:13 ERROR Failed to load Balcón image
2023-05-01 12:03:45 WARN  Disk almost full
2023-05-01 12:05:10 ERROR Señor account locked
2023-05-01 12:07:55 ERROR Timeout on payment gateway
EOF

# Convert to ISO-8859-1 and clean up
RUN iconv -f UTF-8 -t ISO-8859-1 /home/user/logs/session_utf8_temp.log -o /home/user/logs/session_iso8859.log && \
    rm /home/user/logs/session_utf8_temp.log

# Permissions for /home/user
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

LABEL Author="Log-Analysis-Task Preparer"
LABEL Description="Container with initial state for the ISO-8859-1 → UTF-8 log conversion task."

CMD echo "Container for log-conversion task. Run your solution commands here."