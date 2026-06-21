# Author: Apptainer Task Setup
# Description: Container image for the performance benchmark task – provides dataset and Python/pytest.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets/performance

RUN cat > /home/user/datasets/performance/sales_q1.csv <<'EOF'
OrderID,Units,Revenue
1001,5,250
1002,3,150
1003,2,100
EOF

RUN cat > /home/user/datasets/performance/sales_q2.csv <<'EOF'
OrderID,Units,Revenue
2001,4,200
2002,6,300
2003,1,50
EOF

RUN cat > /home/user/datasets/performance/sales_q3.csv <<'EOF'
OrderID,Units,Revenue
3001,7,350
3002,2,100
3003,3,150
EOF

RUN chmod 644 /home/user/datasets/performance/*.csv && \
    chmod 777 /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH