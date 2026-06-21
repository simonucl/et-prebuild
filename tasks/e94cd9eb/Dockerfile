FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/deploy_demo && \
    : > /home/user/deploy_demo/README.md && \
    chmod -R 0775 /home/user/deploy_demo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="$PATH:/usr/local/bin:/usr/bin:/bin"

# Create entrypoint script to set up environment on container start
RUN cat <<'EOF' > /entrypoint.sh
#!/bin/bash
chmod 755 /home/user

# Ensure the required initial state exists each time the container starts.
# This runs as the invoking (non-root) user, guaranteeing correct ownership.
if [ -d /home/user/deploy_demo ]; then
    rm -rf /home/user/deploy_demo
fi

mkdir -p /home/user/deploy_demo
: > /home/user/deploy_demo/README.md
chmod -R u+rwX,go+rX /home/user/deploy_demo

exec "$@"
EOF

RUN chmod +x /entrypoint.sh

WORKDIR /home/user

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]