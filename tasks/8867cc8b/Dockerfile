FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Builder"
LABEL Description="Environment for compliance report generation task with pytest pre-installed."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#############################
# 1. System dependencies
#############################
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    ln -sf /usr/bin/python3 /usr/local/bin/python

#############################
# 2. Python dependencies
#############################
RUN pip3 install --no-cache-dir pytest

#############################
# 3. Create non-privileged user
#############################
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

#############################
# 4. Seed input data
#############################
RUN mkdir -p /home/user/compliance

RUN cat > /home/user/compliance/audit_raw.csv << 'EOF'
system_id,hostname,os,patch_level,encrypted_disk,antivirus_status,last_audit_date
1001,web-01,Ubuntu 20.04,up_to_date,yes,running,2023-09-10
1002,db-01,Ubuntu 18.04,outdated,no,stopped,2023-09-12
1003,app-01,CentOS 7,outdated,yes,running,2023-09-11
1004,web-02,Ubuntu 20.04,up_to_date,no,running,2023-09-09
1005,backup-01,Debian 10,up_to_date,yes,stopped,2023-09-08
1006,legacy-nt,Windows 2008,outdated,no,stopped,2023-09-07
EOF

# Ensure the student can read/write within their home directory
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 700 /home/user/compliance && \
    chmod 644 /home/user/compliance/audit_raw.csv

#############################
# 5. Cleanup
#############################
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user
USER user

CMD ["/bin/bash"]