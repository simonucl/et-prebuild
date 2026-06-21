FROM ubuntu:22.04

# Author user
# Description "Container for transaction-analysis task with pre-loaded CSV and pytest installed."
# This container is prepared for the transaction-analysis exercise.

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN cat >/home/user/data/transactions.csv << 'EOF'
id,product,quantity,price
1,Widget,3,9.99
2,Gadget,2,19.50
3,Doodad,5,4.00
EOF

RUN chmod 777 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/transactions.csv

CMD echo "This container is prepared for the transaction-analysis exercise." && \
    echo "Launch an interactive shell and follow the assignment instructions."