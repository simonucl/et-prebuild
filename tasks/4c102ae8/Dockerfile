FROM ubuntu:22.04

# Author "Automated Build"
# Description "Base image for parallel CSV processing assignment with pytest pre-installed and starter CSV files present."
# This image provides the filesystem state for the parallel CSV processing benchmark assignment.

RUN set -e \
    && apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN cat > /home/user/data/sales_q1.csv <<'EOF'
id,value
1,100
2,200
3,300
4,400
5,500
6,600
7,700
8,800
9,900
10,1000
EOF

RUN cat > /home/user/data/sales_q2.csv <<'EOF'
id,value
1,150
2,250
3,350
4,450
5,550
6,650
7,750
8,850
EOF

RUN cat > /home/user/data/sales_q3.csv <<'EOF'
id,value
1,120
2,220
3,320
4,420
5,520
6,620
7,720
8,820
9,920
10,1020
11,1120
12,1220
EOF

RUN chmod 0777 /home/user \
    && chmod 0644 /home/user/data/sales_q*.csv \
    && chmod 0755 /home/user/data

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="Automated Build"
LABEL Description="Base image for parallel CSV processing assignment with pytest pre-installed and starter CSV files present."