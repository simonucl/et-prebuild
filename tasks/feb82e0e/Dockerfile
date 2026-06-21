FROM ubuntu:22.04

# Help section comments
# Container for CSS colour counting task.
# You are inside the runtime environment.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/assets/css

RUN cat <<'EOF' > /home/user/project/assets/css/style_main.css
body { background-color: #ff0000; color: #00ff00; }
h1   { color: #ff0000; }
p    { border: 1px solid #0000ff; }
EOF

RUN cat <<'EOF' > /home/user/project/assets/css/style_theme.css
.nav    { background: #ABC123; }
.footer { background: #ff0000; }
.btn    { background: #abc123; }
.header { color: #FFF; }   /* 3-digit code must be ignored */
EOF

RUN chmod 777 /home/user/project && \
    chmod 755 /home/user/project/assets && \
    chmod 755 /home/user/project/assets/css && \
    chmod 644 /home/user/project/assets/css/style_main.css && \
    chmod 644 /home/user/project/assets/css/style_theme.css

CMD echo "Container for CSS colour counting task." && \
    echo "You are inside the runtime environment." && \
    exec "$@"