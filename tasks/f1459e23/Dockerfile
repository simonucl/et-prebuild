FROM ubuntu:22.04

# Help:
# This Apptainer image contains:
#   - /home/user/data/sales_q1.csv (raw input)
#   - pytest installed system-wide
# The /home/user/output directory is intentionally absent.

ENV PATH="/usr/local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data

RUN cat <<'EOF' > /home/user/data/sales_q1.csv
Date,Region,Product,Quantity,Unit_Price
2023-01-03,North,Widget,30,9.99
2023-01-05,South,Gadget,20,14.95
2023-02-10,East,Widget,45,9.99
2023-02-14,West,Doohickey,50,4.50
2023-03-01,North,Gadget,25,14.95
2023-03-12,South,Widget,75,9.99
2023-03-20,East,Doohickey,40,4.50
EOF

RUN chmod 0644 /home/user/data/sales_q1.csv

RUN rm -rf /home/user/output

LABEL Author="Your Name"
LABEL Description="Container with raw sales CSV pre-loaded and pytest installed for student exercise."