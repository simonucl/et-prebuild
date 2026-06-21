FROM ubuntu:22.04

# Author "Apptainer setup for security-backup task"
# This container provides the initial environment for the credential-backup
# exercise. The credential files are pre-populated under /home/user/credentials
# and pytest is available for automated grading.

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/credentials && \
    mkdir -p /home/user/backup

RUN cat > /home/user/credentials/db_creds.txt <<'EOF'
username=db_user
password=S3cur3P@ssw0rd
EOF

RUN cat > /home/user/credentials/api_key.txt <<'EOF'
API_KEY=ABCDEF1234567890
EOF

RUN chmod 755 /home/user /home/user/credentials /home/user/backup && \
    chmod 644 /home/user/credentials/db_creds.txt && \
    chmod 644 /home/user/credentials/api_key.txt

LABEL Author="Apptainer setup for security-backup task"