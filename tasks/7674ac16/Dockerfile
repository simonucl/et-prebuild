# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="Prepared by ChatGPT"
LABEL Description="Environment for the Active Users Report task with pytest pre-installed."

# Post section: install dependencies and prepare filesystem
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/admin_data

# Populate accounts.ini using a heredoc
RUN cat > /home/user/admin_data/accounts.ini <<'EOF'
[alice]
status = active
role   = editor

[bob]
status = disabled
role   = admin

[carol]
status = active
role   = viewer

[dave]
status = pending
role   = contributor

[eve]
status = active
role   = admin
EOF

# Set safe permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/admin_data && \
    chmod 0644 /home/user/admin_data/accounts.ini

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH