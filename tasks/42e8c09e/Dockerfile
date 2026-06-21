FROM ubuntu:22.04

# Author: backup-sandbox-preparer
# Description: Environment pre-populated for backup/restore exercise
#
# This container provides the initial filesystem state required for the
# backup/restore exercise. All work must be done inside /home/user at runtime.
# Pytest is installed so the automated grader can verify the initial conditions.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading tests
RUN pip3 install --no-cache-dir pytest

# Prepare initial workspace for the student in /home/user
RUN mkdir -p /home/user/data_to_backup/subdir

# File: /home/user/data_to_backup/report1.txt
RUN cat > /home/user/data_to_backup/report1.txt <<'EOF'
Quarterly revenue report Q1 2024
Total: 1,234,567 USD
EOF

# File: /home/user/data_to_backup/report2.txt
RUN cat > /home/user/data_to_backup/report2.txt <<'EOF'
Quarterly revenue report Q2 2024
Total: 1,345,678 USD
EOF

# File: /home/user/data_to_backup/subdir/config.cfg
RUN cat > /home/user/data_to_backup/subdir/config.cfg <<'EOF'
[settings]
mode=production
version=2.3.4
EOF

# Ensure the files all end with a single trailing newline
RUN sed -i -e '$a\' /home/user/data_to_backup/report1.txt && \
    sed -i -e '$a\' /home/user/data_to_backup/report2.txt && \
    sed -i -e '$a\' /home/user/data_to_backup/subdir/config.cfg

# Make sure the future non-privileged user can work inside /home/user
RUN chmod -R a+rX /home/user && \
    chmod a+rwx /home/user && \
    chmod 755 /home/user

WORKDIR /home/user