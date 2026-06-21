FROM ubuntu:22.04

# Help / runscript content for reference
# Container for Compliance Data Processing task.
# Run your shell commands inside an interactive shell:
#     apptainer exec <container>.sif /bin/bash
#
# Source CSVs:
#   /home/user/compliance_data/transactions_q1.csv
#   /home/user/compliance_data/transactions_q2.csv
#
# Create your output in /home/user/output as per the task instructions.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        csvkit \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/compliance_data

RUN cat <<'EOF' > /home/user/compliance_data/transactions_q1.csv
id,user_id,amount,status,date
1,alice,120.00,COMPLETED,2023-01-15
2,bob,75.50,FAILED,2023-02-03
3,charlie,560.20,COMPLETED,2023-03-22
EOF

RUN cat <<'EOF' > /home/user/compliance_data/transactions_q2.csv
id,user_id,amount,status,date
4,alice,310.00,FAILED,2023-04-02
5,bob,40.00,COMPLETED,2023-05-14
6,diana,88.10,FAILED,2023-06-30
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/compliance_data && \
    chmod 644 /home/user/compliance_data/transactions_q1.csv /home/user/compliance_data/transactions_q2.csv