FROM ubuntu:22.04

# help and labels from %labels
LABEL author="cleaned-csv task setup"
LABEL description="Container seeded with raw CSVs and directory layout for the cleaning assignment."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/raw && \
    mkdir -p /home/user/data/processed && \
    mkdir -p /home/user/benchmark

RUN cat > /home/user/data/raw/dataset1.csv <<'EOF'
id,name,value
1,Alice,10
2,Bob,NA
3,Charlie,30
3,Charlie,30
EOF

RUN cat > /home/user/data/raw/dataset2.csv <<'EOF'
id,score
1,95
2,88
2,88
3,NA
4,76
EOF

RUN chmod -R 0777 /home/user

CMD /bin/sh -c "echo 'Container for CSV-cleaning assignment.' && echo 'You are inside the runtime environment. Refer to the project briefing for instructions.'"