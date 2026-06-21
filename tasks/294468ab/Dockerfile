FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Create directory structure and initial files for the exercise
RUN mkdir -p /home/user/mock_site && \
    mkdir -p /home/user/backup

# Create the HTML file with the exact expected content and newlines
RUN cat >/home/user/mock_site/data.html <<'EOF'
<html>
<body>
<h1>Daily Backup Report</h1>
<p>ARCHIVE: db_full_2023-08-04.tar.gz</p>
<p>ARCHIVE: logs_2023-08-04.tar.gz</p>
<p>STATUS: Completed</p>
</body>
</html>
EOF

# Ensure permissions allow the unprivileged runtime user to write to /home/user/backup
# Give read/execute access to the rest of the created tree
RUN chmod 777 /home/user/backup && \
    chmod 755 /home/user /home/user/mock_site && \
    chmod 644 /home/user/mock_site/data.html

# No special environment variables needed; inherit $HOME from the host

WORKDIR /home/user

CMD ["bash", "-c", "echo 'Container for backup-admin exercise.  Use bash to explore.' && exec \"$@\"", "--"]