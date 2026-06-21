# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package index and install pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && apt-get install -y --no-install-recommends python3-pip && pip3 install --no-cache-dir pytest && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create required directory structure and sample log file
RUN mkdir -p /home/user/logs

# Ensure the student (non-root at runtime) can create /home/user/analysis
RUN chmod 777 /home/user

# Create the authentication sample log with the exact required contents
RUN cat > /home/user/logs/auth_sample.log << 'EOF'
Jan 12 07:21:05 ubuntu sshd[1999]: Failed password for invalid user admin from 203.0.113.5 port 55874 ssh2
Jan 12 07:21:06 ubuntu sshd[1999]: Failed password for invalid user admin from 203.0.113.5 port 55874 ssh2
Jan 12 08:05:11 ubuntu sshd[2032]: Failed password for root from 192.0.2.45 port 42317 ssh2
Jan 12 09:14:33 ubuntu sshd[2099]: Failed password for root from 192.0.2.45 port 42318 ssh2
Jan 12 10:00:00 ubuntu sshd[2105]: Failed password for invalid user test from 198.51.100.23 port 60123 ssh2
Jan 12 10:00:03 ubuntu sshd[2105]: Failed password for invalid user test from 198.51.100.23 port 60123 ssh2
Jan 12 11:55:55 ubuntu sshd[2155]: Failed password for root from 192.0.2.10 port 42109 ssh2
EOF

RUN chmod 755 /home/user/logs
RUN chmod 644 /home/user/logs/auth_sample.log