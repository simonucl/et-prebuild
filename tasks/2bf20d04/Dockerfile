FROM ubuntu:22.04

# Help section not provided; none added

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/deploy

RUN cat >/home/user/deploy/update_app.sh <<'EOF'
#!/bin/bash
echo "Updating application..."
EOF

RUN chmod +x /home/user/deploy/update_app.sh && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD echo "Container for scheduling task prepared."