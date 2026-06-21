FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="ExampleAuthor"
LABEL Description="Container for AWK/Sed host catalogue exercise with initial state prepared."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/provision

RUN cat > /home/user/provision/servers.list <<'EOF'
web-1,10.1.1.10,ubuntu18
web-2,10.1.1.11,ubuntu18
db-1,10.1.2.20,centos7
cache-1,10.1.3.30,alpine3
msg-queue,10.1.4.40,debian10
EOF

RUN chmod 755 /home/user && \
    chmod 775 /home/user/provision && \
    chmod 644 /home/user/provision/servers.list