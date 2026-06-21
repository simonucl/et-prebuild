FROM ubuntu:22.04

# Labels from %labels
LABEL Author="SSH-Hardening-Task"
LABEL Description="Provides initial state and pytest for SSH hardening assessment exercise"

# %post
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/hardening/input && \
    mkdir -p /home/user/hardening/reports && \
    mkdir -p /home/user/hardening/logs && \
    chmod 0777 /home/user && \
    chmod -R 0777 /home/user/hardening

RUN cat >/home/user/hardening/input/ssh_audit.csv <<'EOF'
line_number,hostname,PermitRootLogin,PasswordAuthentication,Port
1,server1,yes,yes,22
2,server2,no,no,2222
3,server3,yes,no,22
4,server4,no,yes,22
EOF

RUN chmod 0644 /home/user/hardening/input/ssh_audit.csv

# %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# %runscript
CMD echo "Container for SSH hardening assessment task." && \
    echo "This image only provides the initial state; execute your solution script separately."