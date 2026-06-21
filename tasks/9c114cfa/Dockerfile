# Converted from Apptainer definition (Bootstrap: localimage)
FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data

RUN cat > /home/user/data/sales_q1.csv <<'EOF'
id,region,sales,week
1,Nort h,200,1
2,South,180,1
3,East,220,1
4,West,210,1
5,North,205,2
6,South,190,2
7,East,230,2
8,West,215,2
9,North,210,3
10,South,195,3
EOF

RUN cat > /home/user/data/sales_q2.csv <<'EOF'
id,region,sales,week
11,East,225,4
12,West,220,4
13,North,215,5
14,South,200,5
15,East,235,6
16,West,225,6
17,North,220,7
EOF

RUN chmod 644 /home/user/data/sales_q1.csv /home/user/data/sales_q2.csv

# Environment section
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run script
CMD /bin/bash -c "echo 'Container for CSV benchmarking task.' && echo 'Inspect /home/user/data for the provided datasets.'"