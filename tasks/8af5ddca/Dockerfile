FROM ubuntu:22.04

# Install Python and pytest
RUN set -ex && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create backup directory structure
RUN mkdir -p /home/user/daily_backup/docs && \
    mkdir -p /home/user/daily_backup/images && \
    mkdir -p /home/user/daily_backup/data && \
    mkdir -p /home/user/reference

# docs/report.txt
RUN cat >/home/user/daily_backup/docs/report.txt <<'EOF'
----------------------------
Quarterly Financial Report
Q1 Revenue: $1,200,000
Q1 Profit: $250,000
----------------------------
EOF

# images/logo.png
RUN printf 'PNGDATA\n' >/home/user/daily_backup/images/logo.png

# data/data.csv
RUN cat >/home/user/daily_backup/data/data.csv <<'EOF'
id,value
1,alpha
2,beta
3,gamma
EOF

# Generate reference SHA-256 digests
RUN cd /home/user/daily_backup && \
    sha256sum docs/report.txt images/logo.png data/data.csv > /home/user/reference/sha256sums.txt

# Ensure readability
RUN chmod -R a+rX /home/user

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="backup-verification-engineer"
LABEL Description="Environment for backup integrity verification task – includes staged files and reference SHA-256 sums."