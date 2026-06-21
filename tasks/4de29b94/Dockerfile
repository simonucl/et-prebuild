FROM ubuntu:22.04

# Basic tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create working directory
RUN mkdir -p /home/user/creds

# current_creds.csv
RUN cat > /home/user/creds/current_creds.csv <<'EOF'
username,service,old_key,expiry,notes
alice,db,AKIAOLDALICE,2023-12-31,rotate soon
bob,web,AKIABOBOLD,2023-10-31,-
carol,cache,AKIACACHEOLD,2023-11-30,urgent
EOF

# new_creds.csv
RUN cat > /home/user/creds/new_creds.csv <<'EOF'
username,service,new_key,issued,valid_until
alice,db,AKIANEWALICE,2023-09-01,2024-09-01
bob,web,AKIANEWB0B,2023-08-15,2024-08-15
carol,cache,AKIANEWCACHE,2023-09-10,2024-09-10
EOF

# Permissions
RUN chmod 777 /home/user/creds && \
    chmod 644 /home/user/creds/current_creds.csv /home/user/creds/new_creds.csv && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH