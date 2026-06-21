FROM ubuntu:22.04

# Install Python tooling required for the test harness
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare the staged support-case directory structure and files
RUN mkdir -p /home/user/support_case/etc/ssh

# auth.log
RUN cat > /home/user/support_case/auth.log << 'EOF'
Jan 12 10:15:42 localhost sshd[1234]: Failed password for invalid user admin from 192.168.1.50 port 54321 ssh2
Jan 12 10:16:00 localhost sshd[1234]: Failed password for root from 192.168.1.60 port 54400 ssh2
Jan 12 10:17:07 localhost sshd[1235]: Accepted publickey for user from 192.168.1.70 port 55000 ssh2
Jan 12 10:18:09 localhost sshd[1236]: Failed password for user from 192.168.1.80 port 56000 ssh2
EOF

# mock_ss_output.txt
RUN cat > /home/user/support_case/mock_ss_output.txt << 'EOF'
Netid State   Recv-Q   Send-Q     Local Address:Port      Peer Address:Port   Process
tcp   LISTEN  0        128        0.0.0.0:22            0.0.0.0:*             123/sshd
tcp   LISTEN  0        128        127.0.0.1:5432        0.0.0.0:*             456/postgres
udp   LISTEN  0        0          0.0.0.0:68            0.0.0.0:*             789/dhclient
tcp   LISTEN  0        128        0.0.0.0:80            0.0.0.0:*             321/httpd
EOF

# etc/ssh/sshd_config
RUN cat > /home/user/support_case/etc/ssh/sshd_config << 'EOF'
Port 22
PermitRootLogin no
PasswordAuthentication yes
EOF

# etc/passwd
RUN cat > /home/user/support_case/etc/passwd << 'EOF'
root:x:0:0:root:/root:/bin/bash
user:x:1000:1000:user:/home/user:/bin/bash
EOF

# Permissions
RUN chmod -R 755 /home/user && \
    chmod 777 /home/user/support_case

ENV PYTHONUNBUFFERED=1