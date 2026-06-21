FROM ubuntu:22.04

# Install required tools
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip rsync

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory layout
RUN mkdir -p /home/user/datasets/raw && \
    mkdir -p /home/user/remote_server/datasets_backup

# customers.csv
RUN cat > /home/user/datasets/raw/customers.csv <<'EOF'
id,name,age
1,Alice,30
2,Bob,25
3,Charlie,35
EOF

# sales.csv
RUN cat > /home/user/datasets/raw/sales.csv <<'EOF'
order_id,customer_id,amount
1001,1,250.50
1002,2,150.00
1003,3,300.00
EOF

# Permissions
RUN chmod -R 777 /home/user

# Equivalent of %runscript (runtime command)
CMD chmod 755 /home/user && echo "Container for rsync exercise ready."