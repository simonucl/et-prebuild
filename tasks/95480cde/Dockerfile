# Converted from Apptainer definition (Bootstrap: localimage)
FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Prepare challenge artefacts
RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user

# Suspicious IP list
RUN cat > /home/user/suspicious_ips.txt <<'EOF'
203.0.113.45
198.51.100.77
192.0.2.13
EOF

# Partial auth.log
RUN cat > /home/user/logs/auth.log <<'EOF'
Jan  1 10:01:15 server sshd[12345]: Failed password for invalid user admin from 203.0.113.45 port 54321 ssh2
Jan  1 10:02:09 server sshd[12346]: Failed password for invalid user root from 198.51.100.77 port 54322 ssh2
Jan  1 10:05:30 server sshd[12347]: Failed password for invalid user admin from 203.0.113.45 port 54323 ssh2
Jan  1 10:07:42 server sshd[12348]: Failed password for invalid user test from 203.0.113.45 port 54324 ssh2
Jan  1 10:12:03 server sshd[12349]: Failed password for invalid user guest from 198.51.100.77 port 54325 ssh2
Jan  1 10:15:29 server sshd[12350]: Failed password for invalid user ubuntu from 203.0.113.45 port 54326 ssh2
EOF

RUN chmod 0644 /home/user/suspicious_ips.txt /home/user/logs/auth.log && \
    chmod 0755 /home/user/logs

# Environment variables from %environment
# Original chmod command omitted because Docker ENV cannot execute commands
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"