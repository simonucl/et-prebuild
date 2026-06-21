FROM ubuntu:22.04

# Author="Apptainer Task Setup"
# Description="Environment prepared for the East Widget sales extraction task with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/datasets

RUN cat > /home/user/datasets/sales_q1.csv <<'EOF'
Date,Region,Product,Units,Unit_Price
2023-01-05,East,Widget A,120,9.50
2023-01-07,West,Widget B,200,9.50
2023-02-11,East,Thingamajig,75,15.00
2023-03-02,East,Widget Pro,60,12.00
2023-03-09,South,Widget A,110,9.50
EOF

RUN cat > /home/user/datasets/sales_q2.csv <<'EOF'
Date,Region,Product,Units,Unit_Price
2023-04-15,East,Widget A,90,9.50
2023-05-03,North,Gadget,150,8.00
2023-05-22,East,Widget Plus,50,11.00
2023-06-12,East,Thingamajig,40,15.00
2023-06-25,West,Widget A,130,9.50
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/datasets && \
    chmod 644 /home/user/datasets/sales_q1.csv /home/user/datasets/sales_q2.csv && \
    rm -rf /home/user/output || true

ENV PYTHONUNBUFFERED=1