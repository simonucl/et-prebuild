FROM ubuntu:22.04

# Container for the “SSH login summary” exercise.
# Pre-installs pytest and seeds /home/user/logs/auth.log with the required data.

ENV PYTHONIOENCODING=UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    mkdir -p /home/user/logs && \
    chmod 777 /home/user && \
    chmod 755 /home/user/logs

RUN cat > /home/user/logs/auth.log <<'EOF'
Jan 10 10:00:00 localhost sshd[12345]: Accepted password for alice from 192.168.1.5 port 52222 ssh2
Jan 10 10:00:05 localhost sshd[12346]: Failed password for bob from 192.168.1.6 port 52223 ssh2
Jan 10 10:00:10 localhost sshd[12347]: Failed password for alice from 192.168.1.7 port 52224 ssh2
Jan 10 10:00:15 localhost sshd[12348]: Accepted password for carol from 192.168.1.8 port 52225 ssh2
Jan 10 10:00:20 localhost sshd[12349]: Failed password for carol from 192.168.1.9 port 52226 ssh2
Jan 10 10:00:25 localhost sshd[12350]: Accepted password for bob from 192.168.1.10 port 52227 ssh2
Jan 10 10:00:30 localhost sshd[12351]: Accepted password for alice from 192.168.1.11 port 52228 ssh2
Jan 10 10:00:35 localhost sshd[12352]: Failed password for dave from 192.168.1.12 port 52229 ssh2
EOF

RUN chmod 644 /home/user/logs/auth.log