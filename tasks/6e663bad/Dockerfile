# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Converted from Apptainer definition
# ------------------------------------------------------------

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    install -d -m 0700 /home/user/logs

RUN cat > /home/user/logs/auth.log << 'EOF'
Jan 10 12:05:10 server sshd[1234]: Accepted password for alice from 192.168.0.2 port 54022 ssh2
Jan 10 12:07:15 server sshd[1235]: Failed password for bob from 192.168.0.3 port 54023 ssh2
Jan 10 12:08:45 server sshd[1236]: Accepted password for bob from 192.168.0.3 port 54023 ssh2
Jan 10 12:15:01 server sshd[1237]: Failed password for charlie from 192.168.0.4 port 54024 ssh2
Jan 10 12:16:35 server sshd[1238]: Failed password for charlie from 192.168.0.4 port 54024 ssh2
Jan 10 12:16:39 server sshd[1239]: Failed password for charlie from 192.168.0.4 port 54024 ssh2
Jan 10 12:16:40 server sshd[1239]: ACCOUNT LOCKED: charlie; too many failures
Jan 10 12:18:12 server sshd[1240]: Accepted password for alice from 192.168.0.2 port 54022 ssh2
Jan 10 13:01:09 server sshd[1241]: Failed password for bob from 192.168.0.3 port 54023 ssh2
Jan 10 13:05:22 server sshd[1242]: Accepted password for dave from 192.168.0.5 port 54025 ssh2
Jan 10 14:22:33 server sshd[1243]: Failed password for dave from 192.168.0.5 port 54025 ssh2
Jan 10 14:25:37 server sshd[1244]: password expired for eve; account needs password change
Jan 10 14:25:38 server sshd[1245]: Accepted password for eve from 192.168.0.6 port 54026 ssh2
Jan 10 14:30:01 server sshd[1246]: Failed password for alice from 192.168.0.2 port 54022 ssh2
EOF

RUN chmod 0644 /home/user/logs/auth.log && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD ["/bin/bash"]