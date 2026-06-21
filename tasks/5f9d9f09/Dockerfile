# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest for the validation suite
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare the initial filesystem state for the compliance exercise
# ------------------------------------------------------------------
# 1. Create the audit directory and make sure every non-privileged
#    user inside the container can write to it.
RUN mkdir -p /home/user/audit && \
    chmod 0777 /home/user/audit

# 2. Populate the canonical sample syslog with exactly 13 lines.
RUN cat > /home/user/audit/syslog_sample.log <<'EOF'
Jan 12 14:35:02 server1 sshd[1024]: Failed password for invalid user admin from 192.168.1.25 port 54421 ssh2
Jan 12 14:36:15 server1 sshd[1025]: Session opened for user root by (uid=0)
Jan 12 14:37:20 server1 sshd[1025]: Session closed for user root
Jan 12 14:40:55 server1 sshd[1030]: Failed password for root from 192.168.1.26 port 54422 ssh2
Jan 12 14:42:03 server1 sshd[1031]: Accepted password for user bob from 192.168.1.27 port 54423 ssh2
Jan 12 14:42:04 server1 sshd[1031]: session opened for user bob by (uid=0)
Jan 12 14:45:10 server1 sudo: pam_unix(sudo:session): session opened for user root by bob(uid=0)
Jan 12 14:46:33 server1 sshd[1036]: Failed password for invalid user guest from 192.168.1.28 port 54424 ssh2
Jan 12 14:48:57 server1 sshd[1040]: Failed password for root from 192.168.1.29 port 54425 ssh2
Jan 12 14:49:01 server1 sshd[1040]: Failed password for root from 192.168.1.29 port 54425 ssh2
Jan 12 14:50:12 server1 sshd[1045]: Session opened for user root by (uid=0)
Jan 12 14:51:20 server1 sshd[1045]: Session closed for user root
Jan 12 14:52:30 server1 sshd[1050]: Failed password for invalid user test from 192.168.1.30 port 54426 ssh2
EOF

RUN chmod 0644 /home/user/audit/syslog_sample.log

# ------------------------------------------------------------------
# Environment setup (from %environment)
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# Help / runscript behavior
# ------------------------------------------------------------------
CMD echo "Container for the 'Compliance scenario – simple regex-based log filtering' prepared." && \
    echo "You can now run your commands inside the container."