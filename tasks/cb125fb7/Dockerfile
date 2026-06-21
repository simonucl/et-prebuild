FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer setup script"
LABEL Description="Environment for the 'sales aggregation' exercise — includes pytest and initial data."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# 1. Install required packages and Python tooling
RUN set -eux && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        time \
        parallel \
        ca-certificates \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Set-up working directory structure under /home/user
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    chmod 0777 /home/user/output

# 3. Populate the three quarter CSV files with the exact specification
RUN cat <<'EOF' > /home/user/data/sales_q1.csv
Region,Product,Units,UnitPrice
North,Widget,10,20.5
South,Gadget,5,15
East,Widget,7,20.5
North,Gadget,3,15
EOF

RUN cat <<'EOF' > /home/user/data/sales_q2.csv
Region,Product,Units,UnitPrice
South,Widget,8,20.5
East,Gadget,6,15
West,Widget,4,20.5
North,Widget,11,20.5
EOF

RUN cat <<'EOF' > /home/user/data/sales_q3.csv
Region,Product,Units,UnitPrice
East,Widget,9,20.5
South,Gadget,2,15
West,Gadget,5,15
North,Gadget,7,15
EOF

# Ensure readable by all
RUN chmod 0644 /home/user/data/sales_q*.csv

# 4. Create an unprivileged user 'user'
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    chmod 755 /home/user

WORKDIR /home/user