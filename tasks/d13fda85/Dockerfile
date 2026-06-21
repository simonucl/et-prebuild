FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/logs

# auth.log.2023-07-17
RUN cat > /home/user/logs/auth.log.2023-07-17 <<'EOF'
Jul 17 02:15:43 server sshd[12345]: Failed password for invalid user admin from 192.168.1.5 port 53422 ssh2
Jul 17 04:20:11 server sshd[12346]: Accepted password for user1 from 10.0.0.3 port 41414 ssh2
Jul 17 14:55:01 server sshd[12347]: Failed password for root from 203.0.113.8 port 62119 ssh2
Jul 17 18:37:29 server sshd[12348]: Failed password for invalid user test from 198.51.100.23 port 33788 ssh2
EOF

# auth.log.2023-07-18
RUN cat > /home/user/logs/auth.log.2023-07-18 <<'EOF'
Jul 18 03:05:13 server sshd[22345]: Failed password for root from 198.51.100.23 port 42312 ssh2
Jul 18 05:30:55 server sshd[22346]: Failed password for invalid user guest from 203.0.113.8 port 61311 ssh2
Jul 18 05:31:02 server sshd[22347]: Failed password for invalid user guest from 203.0.113.8 port 61312 ssh2
Jul 18 10:01:11 server sshd[22348]: Accepted password for user2 from 10.0.0.4 port 33899 ssh2
EOF

# auth.log.2023-07-19
RUN cat > /home/user/logs/auth.log.2023-07-19 <<'EOF'
Jul 19 07:42:00 server sshd[32345]: Failed password for invalid user admin from 192.168.1.5 port 52013 ssh2
Jul 19 07:42:09 server sshd[32346]: Failed password for invalid user admin from 192.168.1.5 port 52014 ssh2
Jul 19 09:15:00 server sshd[32347]: Failed password for root from 198.51.100.23 port 63321 ssh2
Jul 19 15:21:42 server sshd[32348]: Failed password for invalid user test from 203.0.113.8 port 31114 ssh2
Jul 19 20:01:17 server sshd[32349]: Accepted password for user3 from 10.0.0.5 port 22555 ssh2
EOF

# Set correct permissions on the log files
RUN chmod 0644 /home/user/logs/auth.log.2023-07-17 && \
    chmod 0644 /home/user/logs/auth.log.2023-07-18 && \
    chmod 0644 /home/user/logs/auth.log.2023-07-19

# Ensure ownership is root, but everything is world-readable as required
RUN chown -R root:root /home/user

# Set permissions on /home/user at runtime and environment variables
RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1