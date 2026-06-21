FROM ubuntu:22.04

# help text
# This container provides the initial environment for the incident-response
# exercise. The student will analyze /home/user/logs/auth.log and create
# /home/user/ir/failures.log as specified. Pytest is installed so that the
# provided test suite can verify the initial state.

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -eux && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat > /home/user/logs/auth.log <<'EOF'
Nov  5 10:15:42 ubuntu sshd[12345]: Failed password for invalid user admin from 192.168.1.10 port 54321 ssh2
Nov  5 10:15:45 ubuntu sshd[12346]: Failed password for invalid user root from 192.168.1.10 port 54322 ssh2
Nov  5 10:15:50 ubuntu sshd[12347]: Failed password for invalid user admin from 192.168.1.10 port 54321 ssh2
Nov  5 10:16:00 ubuntu sshd[12348]: Failed password for invalid user guest from 192.168.1.20 port 54323 ssh2
Nov  5 10:16:05 ubuntu sshd[12349]: Failed password for invalid user guest from 192.168.1.20 port 54323 ssh2
Nov  5 10:17:10 ubuntu sshd[12350]: Failed password for invalid user test from 203.0.113.5 port 60001 ssh2
Nov  6 09:01:12 ubuntu sshd[22345]: Failed password for invalid user admin from 192.168.1.10 port 54324 ssh2
EOF

RUN chmod 0644 /home/user/logs/auth.log

RUN chmod 755 /home/user

LABEL Author="incident-response-setup" \
      Description="Container for incident-response analyst task with ground-truth SSH auth.log and pytest installed."