# Author: AutomatedSetup
# Description: Environment for CSV-to-TSV column-reformatting task.
# This container provides the starting environment for the CSV→TSV column-extraction task.
# The file /home/user/data/raw_contacts.csv is pre-populated exactly as specified, and pytest is available for automated tests.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN cat > /home/user/data/raw_contacts.csv <<'EOF'
id,name,email,department
1,Alice Anderson,alice.anderson@example.com,Finance
2,Bob Brown,bob.brown@example.com,Engineering
3,Charlie Clark,charlie.clark@example.com,Marketing
EOF

RUN chmod 0777 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8