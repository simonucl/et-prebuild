FROM ubuntu:22.04

# Help: Container for DevSecOps port-compliance exercise.

RUN set -e && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN mkdir -p /home/user/policies

RUN cat > /home/user/policies/service_ports.csv <<'EOF'
service,port
ssh,22
http,80
https,443
custom-app,8080
db-mysql,3306
db-postgres,5432
old-telnet,23
custom-admin,10022
dev-service,12000
EOF

RUN chmod 644 /home/user/policies/service_ports.csv

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"

CMD echo "Container for DevSecOps port-compliance exercise. Open a shell to begin."