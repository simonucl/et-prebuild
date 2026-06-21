FROM ubuntu:22.04

# Help: Default runscript does nothing; container is meant for interactive use

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/incident

RUN cat > /home/user/incident/.env.incident <<'EOF'
DB_USER=central
DB_PASS=R3sp0nder!
INCIDENT_ID=ZA-8841
API_TOKEN=762f4e86-9d48-4d6a-8e63-25f00ec3f3c9
EOF

RUN chmod 0664 /home/user/incident/.env.incident && \
    chmod 0777 /home/user/incident && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin