# Author AI_Assistant
# Description "Initial state for 2020 quarterly sales ETL coding task"
# Help:
# This container provides the starting point for the "2020 quarterly sales
# ETL" programming task. The four required raw CSV files are pre-populated
# under /home/user/data/raw/, and no other task-related directories or
# output files exist yet. Pytest is available for running the supplied
# test suite.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/raw

RUN cat <<'EOF' > /home/user/data/raw/sales_q1_2020.csv
Region,Country,SalesPerson,Product,Units,UnitPrice
EMEA,Germany,Anna Schmidt,Widget A,120,25.50
APAC,Japan,Kenji Ito,Widget B,85,30.00
EOF

RUN cat <<'EOF' > /home/user/data/raw/sales_q2_2020.csv
Region,Country,SalesPerson,Product,Units,UnitPrice
EMEA,France,Jean Dupont,Widget A,95,25.50
AMER,USA,Maria Garcia,Widget C,150,45.00
EOF

RUN cat <<'EOF' > /home/user/data/raw/sales_q3_2020.csv
Region,Country,SalesPerson,Product,Units,UnitPrice
APAC,Australia,Liam Brown,Widget B,130,30.00
AMER,Canada,Noah Wilson,Widget A,110,25.50
EOF

RUN cat <<'EOF' > /home/user/data/raw/sales_q4_2020.csv
Region,Country,SalesPerson,Product,Units,UnitPrice
EMEA,Italy,Luca Rossi,Widget C,140,45.00
APAC,China,Wei Zhang,Widget A,200,25.50
EOF

RUN chmod 0644 /home/user/data/raw/sales_q?_2020.csv && \
    chmod -R a+rX /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

CMD ["/bin/bash"]