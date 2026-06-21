FROM ubuntu:22.04

# Help text from %help (none provided in this file)

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

RUN cat <<'EOF' >/home/user/service_mappings.csv
Service,OldURL,NewURL
auth,https://old.example.com/auth,https://api.new-corp.io/auth
billing,https://old.example.com/bill,https://api.new-corp.io/billing
catalog,https://old.example.com/catalog,https://api.new-corp.io/catalog
inventory,https://old.example.com/inv,https://api.new-corp.io/inventory
shipping,https://old.example.com/ship,https://api.new-corp.io/shipping
EOF

RUN chmod 644 /home/user/service_mappings.csv && \
    chmod 755 /home/user

CMD echo "Container for CSV-to-report migration task. Execute your commands inside an interactive shell."