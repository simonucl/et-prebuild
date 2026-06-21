FROM ubuntu:22.04

# System packages & Python tooling
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends rsync python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create an unprivileged user (`user`, uid/gid 1000)
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Prepare the initial filesystem state
# Directory structure – permissions are 755
RUN install -d -m 0755 /home/user/remote_host_sim/app_logs && \
    install -d -m 0755 /home/user/local_backup/app_logs

# Remote "*.log" & "*.tmp" files with exact contents – permissions 644
RUN cat > /home/user/remote_host_sim/app_logs/app-2023-10-01.log <<'EOF'
LOG-A
EOF

RUN cat > /home/user/remote_host_sim/app_logs/app-2023-10-02.log <<'EOF'
LOG-B
EOF

RUN cat > /home/user/remote_host_sim/app_logs/debug-2023-10-01.log <<'EOF'
DEBUG-A
EOF

RUN cat > /home/user/remote_host_sim/app_logs/session.tmp <<'EOF'
TEMP
EOF

RUN chmod 0644 /home/user/remote_host_sim/app_logs/*

# Ownership - Make sure the unprivileged user owns everything under /home/user
RUN chown -R 1000:1000 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set permissions on /home/user at runtime and default shell
RUN chmod 755 /home/user

CMD ["/bin/bash"]