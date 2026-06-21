FROM ubuntu:22.04

# Help / runscript note
# Apptainer image ready for the sudo audit task. Drop into a shell with 'apptainer exec' if needed.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/audit_logs/raw

RUN cat <<'EOF_AUTH' > /home/user/audit_logs/raw/auth.log
Oct  1 14:32:18 ubuntu2004 sudo:    alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/bin/apt update
Oct  1 15:01:03 ubuntu2004 sudo:    bob : TTY=pts/1 ; PWD=/home/bob ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx
Oct  1 16:45:55 ubuntu2004 sudo:    charlie : TTY=pts/2 ; PWD=/home/charlie ; USER=root ; COMMAND=/bin/cat /etc/shadow
Oct  2 08:11:08 ubuntu2004 sshd[4242]: Failed password for invalid user guest from 203.0.113.9 port 52892 ssh2
Oct  2 09:27:44 ubuntu2004 CRON[4321]: pam_unix(cron:session): session closed for user root
EOF_AUTH

RUN : > /home/user/audit_logs/raw/syslog

RUN chmod -R a+rX /home/user && \
    chmod a+w /home/user/audit_logs && \
    chmod a+w /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin