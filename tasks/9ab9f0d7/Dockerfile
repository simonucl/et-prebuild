FROM ubuntu:22.04

# Author: DevSecOps-Task-Setup
# Description: Initial dataset and tooling for CSV-to-TSV transformation exercise.

ENV PATH="/home/user/.local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then useradd -m -d /home/user -s /bin/bash user; fi && \
    mkdir -p /home/user/company_logs

RUN cat >/home/user/company_logs/policy_violations.csv <<'EOF'
date,user,policy,severity,action,status
2023-06-01,alice,SSH Root Login,Critical,Alert,OPEN
2023-06-02,bob,Password Reuse,High,Block,CLOSED
2023-06-03,carol,Public S3 Bucket,Medium,Alert,OPEN
2023-06-03,dave,Unencrypted S3 Bucket,High,Alert,OPEN
2023-06-04,erin,Insecure Protocol,Critical,Block,CLOSED
2023-06-05,frank,Outdated SSL Cert,Medium,Alert,OPEN
2023-06-06,grace,Open Security Group,High,Alert,OPEN
2023-06-07,heidi,Missing MFA,Critical,Alert,CLOSED
EOF

RUN cat >/home/user/company_logs/active_employees.txt <<'EOF'
alice
carol
dave
frank
grace
mallory
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/company_logs && \
    chmod 644 /home/user/company_logs/policy_violations.csv && \
    chmod 644 /home/user/company_logs/active_employees.txt && \
    chown -R user:user /home/user