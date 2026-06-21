FROM ubuntu:22.04

# Install Python tooling required by the automated grader
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure and seed the sample auth.log file
RUN mkdir -p /home/user/log_samples

RUN cat <<'EOF' > /home/user/log_samples/auth.log
Jan 10 12:00:01 localhost CRON[1011]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Jan 10 12:01:45 localhost sshd[1024]: Failed password for invalid user admin from 192.168.1.20 port 54321 ssh2
Jan 10 12:02:10 localhost sshd[1024]: Accepted password for user1 from 192.168.1.2 port 54322 ssh2
Jan 10 12:03:22 localhost sshd[1024]: Invalid user test from 192.168.1.21
Jan 10 12:03:45 localhost sshd[1027]: Connection closed by authenticating user user1 192.168.1.2 port 54323 [preauth]
Jan 10 12:04:57 localhost sudo: pam_unix(sudo:auth): authentication failure; logname=user1 uid=1000 euid=0 tty=/dev/pts/0 ruser=user1 rhost=  user=user1
Jan 10 12:05:02 localhost sudo:   user1 : TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/bin/ls
Jan 10 12:06:13 localhost sshd[1030]: Failed password for root from 203.0.113.55 port 60001 ssh2
Jan 10 12:07:44 localhost sshd[1031]: Received disconnect from 192.168.1.3 port 54324:11: disconnected by user
Jan 10 12:08:12 localhost sshd[1032]: Invalid user backup from 192.168.1.25
Jan 10 12:08:35 localhost sshd[1033]: Failed password for invalid user cisco from 203.0.113.77 port 60005 ssh2
Jan 10 12:09:57 localhost sshd[1034]: Accepted publickey for deploy from 192.168.1.4 port 54326 ssh2: RSA SHA256:xyz
Jan 10 12:10:11 localhost sudo: pam_unix(sudo:auth): (user2) : authentication failure; logname=user2 uid=1001 euid=0 tty=/dev/pts/1 ruser=user2 rhost=  user=user2
Jan 10 12:11:05 localhost CRON[1040]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Jan 10 12:12:44 localhost sshd[1042]: Failed password for root from 198.51.100.10 port 62000 ssh2
Jan 10 12:14:22 localhost sshd[1043]: Invalid user oracle from 192.168.1.26
Jan 10 12:15:33 localhost sshd[1044]: Failed password for invalid user postgres from 203.0.113.88 port 60010 ssh2
Jan 10 12:16:54 localhost sshd[1045]: Connection closed by 192.168.1.4 port 54327 [preauth]
Jan 10 12:18:01 localhost sudo:   user2 : TTY=pts/1 ; PWD=/home/user ; USER=root ; COMMAND=/usr/bin/apt update
Jan 10 12:19:45 localhost sshd[1046]: Failed password for root from 192.168.1.30 port 62001 ssh2
EOF

RUN chmod 644 /home/user/log_samples/auth.log && \
    chmod 755 /home/user /home/user/log_samples

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Help text (from %runscript)
# Container for the authentication-log hardening exercise.
# Invoke 'docker run -it <image> bash' to obtain a shell.