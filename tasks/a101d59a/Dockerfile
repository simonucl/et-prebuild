FROM ubuntu:22.04

# Labels
LABEL Author="Automated build for disk-usage analysis task"
LABEL Description="Base image containing pre-seeded quarterly sales CSV files and pytest"

# Post section
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/data/csvs && \
    chmod 0755 /home && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data && \
    chmod 0755 /home/user/data/csvs

RUN cat > /home/user/data/csvs/sales_2021_q1.csv <<'EOF'
Region,Product,Units
North,Widget,100
South,Gadget,150
East,Widget,200
EOF

RUN cat > /home/user/data/csvs/sales_2021_q2.csv <<'EOF'
Region,Product,Units
West,Widget,120
North,Gadget,110
South,Widget,90
East,Gadget,130
EOF

RUN cat > /home/user/data/csvs/sales_2021_q3.csv <<'EOF'
Region,Product,Units
North,Widget,140
West,Gadget,160
EOF

RUN chmod 0644 /home/user/data/csvs/sales_2021_q1.csv && \
    chmod 0644 /home/user/data/csvs/sales_2021_q2.csv && \
    chmod 0644 /home/user/data/csvs/sales_2021_q3.csv

# Environment section
RUN chmod 755 /home/user
ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8