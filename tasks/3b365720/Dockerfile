FROM ubuntu:22.04

# Help text
# Author="Container builder"
# Description="Environment for 'system-snapshot & CSV business summary' assignment. Includes pytest and sample dataset."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    chmod -R 0777 /home/user

RUN cat >/home/user/data/transactions.csv <<'CSV_EOF'
transaction_id,customer_id,amount,currency
T001,C001,100,USD
T002,C002,250,USD
T003,C001,75,USD
T004,C003,300,USD
T005,C002,150,USD
CSV_EOF

RUN chmod 0666 /home/user/data/transactions.csv

RUN chmod 755 /home/user

ENV PATH="$PATH:$HOME/.local/bin"

CMD /bin/sh -c "echo 'Container for the assignment is ready.' && echo 'Navigate to /home/user to start working.'"