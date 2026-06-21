FROM ubuntu:22.04

# Author batch-summary-setup
# Container image primed for the "batch summary" command-line exercise.
# Includes:
#   • Prepared /home/user/data/reports/ with three CSV input files.
#   • Pytest installed for the automated test harness.
# The /home/user/output directory is intentionally omitted so that the
# learner's solution creates it afresh.

# ------------------------------------------------------------------
# Basic packages and Python tooling for the test-runner
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gawk \
        findutils \
        coreutils && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create non-privileged user "user" with home at /home/user
# ------------------------------------------------------------------
RUN set -e && \
    if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash -u 1000 -g user user; \
    fi && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Set up the required input directory tree and CSV files
# ------------------------------------------------------------------
RUN mkdir -p /home/user/data/reports && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/data/reports

RUN cat > /home/user/data/reports/report_202301.csv << 'EOF'
id,value,comment
1,10,good
2,20,
3,,missing
EOF

RUN cat > /home/user/data/reports/report_202302.csv << 'EOF'
id,value,comment
a1,5,low
a2,15,mid
a3,25,high
EOF

RUN cat > /home/user/data/reports/report_202303.csv << 'EOF'
id,value,comment
x1,,
x2,50,okay
x3,60,
EOF

RUN chmod 644 /home/user/data/reports/report_202301.csv && \
    chmod 644 /home/user/data/reports/report_202302.csv && \
    chmod 644 /home/user/data/reports/report_202303.csv

# ------------------------------------------------------------------
# Ensure the output directory is absent so tests start with a clean slate
# ------------------------------------------------------------------
RUN if [ -d /home/user/output ]; then \
        rm -rf /home/user/output; \
    fi

# Give ownership of everything under /home/user to the "user" account
RUN chown -R user:user /home/user