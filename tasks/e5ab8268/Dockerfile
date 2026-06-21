FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state required by the assignment
RUN mkdir -p /home/user/sample_logs

RUN cat > /home/user/sample_logs/system.log <<'EOF'
Jul 10 11:23:56 server sshd[2345]: Failed password for invalid user admin from 10.0.0.55 port 54322 ssh2
Jul 10 11:23:58 server sshd[2346]: Failed password for invalid user admin from 10.0.0.55 port 54323 ssh2
Jul 10 11:24:02 server sshd[2347]: Accepted password for user1 from 192.168.1.10 port 54411 ssh2
Jul 10 11:25:01 server sshd[2348]: Failed password for invalid user root from 203.0.113.99 port 51720 ssh2
Jul 10 11:25:13 server sshd[2351]: Failed password for root from 203.0.113.99 port 51721 ssh2
Jul 10 11:26:30 server sshd[2355]: Failed password for invalid user admin from 10.0.0.55 port 54324 ssh2
Jul 10 11:27:00 server cron[1111]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)
Jul 10 11:28:45 server sshd[2359]: Failed password for root from 198.51.100.77 port 51800 ssh2
EOF

# Set permissions: log file readable, directory accessible
RUN chmod 0644 /home/user/sample_logs/system.log && \
    chmod 0755 /home/user/sample_logs && \
    chmod 755 /home/user

# Labels
LABEL Author="incident-log-container"
LABEL Description="Container with initial SSH log for incident triage task"

# Help: This container ships a prepared /home/user/sample_logs/system.log file
# and has pytest pre-installed so that automated grading scripts can run.