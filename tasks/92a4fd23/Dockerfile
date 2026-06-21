FROM ubuntu:22.04

# Help / metadata
LABEL Author="Apptainer Task Prepper"
LABEL Description="Environment for CSV cleaning task with initial raw data and pytest installed."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/raw && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data && \
    chmod 0777 /home/user/data/raw

RUN cat > /home/user/data/raw/customers.csv <<'EOF'
id,name,age,country
1,Alice,31,US
2,Bob,25,CA
3,Charlie,35,UK
4,David,28,US
EOF

RUN chmod 0644 /home/user/data/raw/customers.csv

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH