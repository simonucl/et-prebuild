FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establish the required initial filesystem state for the exercise

# 1. Ensure the base home directory exists
RUN mkdir -p /home/user && \
    chmod 0755 /home/user

# 2. Create the incoming directory with strict permissions
RUN mkdir -p /home/user/incoming && \
    chmod 0700 /home/user/incoming

# 3. Create the CSV file with exact required contents
RUN cat > /home/user/incoming/artifact_inventory.csv <<'EOF'
id,name,repository,sha256,status
1,alpha,stable-core,111aaa,approved
2,beta,testing-core,222bbb,rejected
3,gamma,stable-core,333ccc,approved
4,delta,stable-utils,444ddd,approved
5,epsilon,stable-core,555eee,pending
6,zeta,experimental,666fff,approved
7,eta,stable-utils,777ggg,rejected
8,theta,stable-core,888hhh,approved
EOF

# 4. Set the strict permissions on the CSV
RUN chmod 0600 /home/user/incoming/artifact_inventory.csv

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8