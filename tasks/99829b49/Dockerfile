FROM ubuntu:22.04

# Help section
# Default to an interactive shell if the container is run without args

ENV PATH="/root/.local/bin:${PATH}"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/cloud/reports && \
    chmod 0777 /home/user/cloud/reports && \
    mkdir -p /home/user

RUN cat > /home/user/cloud/costs.ini <<'EOF'
[vm1]
status=active
env=dev
cost=12.34

[db1]
status=inactive
env=dev
cost=5.00

[web1]
status=active
env=staging
cost=20.00

[cache1]
status=active
env=prod
cost=15.50

[queue1]
status=inactive
env=prod
cost=3.00
EOF

RUN chmod 0644 /home/user/cloud/costs.ini && \
    chmod 755 /home/user

CMD ["/bin/bash"]