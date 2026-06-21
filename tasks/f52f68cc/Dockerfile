FROM ubuntu:22.04

# Help section (from %help if present)

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g user user

RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output

RUN cat > /home/user/data/usage.csv <<'EOF'
host,timestamp,cpu,memory
host1,2023-01-01T00:00:00Z,57,40
host1,2023-01-01T01:00:00Z,63,43
host1,2023-01-01T02:00:00Z,50,38
host2,2023-01-01T00:00:00Z,80,70
host2,2023-01-01T01:00:00Z,75,68
host2,2023-01-01T02:00:00Z,82,71
host3,2023-01-01T00:00:00Z,20,30
host3,2023-01-01T01:00:00Z,25,28
host3,2023-01-01T02:00:00Z,22,29
EOF

RUN chown -R user:user /home/user && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data && \
    chmod 0755 /home/user/output && \
    chmod 0644 /home/user/data/usage.csv

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin