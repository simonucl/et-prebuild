FROM ubuntu:22.04

# Help:
# This container provides the environment for:
# “Compliance audit – failed SSH log-in summary”
# Contents:
# - /home/user/audit_logs/auth.log (12 SSH failure lines)
# - pytest installed
# Goal: Generate /home/user/audit_logs/compliance_summary.csv

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/audit_logs && \
    chmod 0777 /home/user/audit_logs

RUN cat >/home/user/audit_logs/auth.log <<'EOF'
Jan 10 10:01:02 server sshd[12345]: Failed password for invalid user admin from 203.0.113.10 port 54321 ssh2
Jan 10 10:05:22 server sshd[12346]: Failed password for invalid user test from 198.51.100.42 port 54421 ssh2
Jan 10 10:07:11 server sshd[12347]: Failed password for root from 203.0.113.10 port 54456 ssh2
Jan 10 10:15:45 server sshd[12348]: Failed password for invalid user guest from 203.0.113.10 port 54671 ssh2
Jan 10 11:20:13 server sshd[12349]: Failed password for invalid user admin from 192.0.2.77 port 54781 ssh2
Jan 10 12:25:39 server sshd[12350]: Failed password for invalid user user from 198.51.100.42 port 54931 ssh2
Jan 10 13:02:54 server sshd[12351]: Failed password for root from 198.51.100.42 port 55043 ssh2
Jan 10 15:14:22 server sshd[12352]: Failed password for invalid user admin from 203.0.113.10 port 55211 ssh2
Jan 10 16:55:03 server sshd[12353]: Failed password for invalid user admin from 198.51.100.42 port 55344 ssh2
Jan 10 17:35:49 server sshd[12354]: Failed password for invalid user guest from 198.51.100.42 port 55433 ssh2
Jan 10 18:42:05 server sshd[12355]: Failed password for root from 203.0.113.10 port 55510 ssh2
Jan 10 19:12:37 server sshd[12356]: Failed password for invalid user noob from 192.0.2.77 port 55688 ssh2
EOF

RUN chmod 0644 /home/user/audit_logs/auth.log

RUN chmod 755 /home/user || true

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1