FROM ubuntu:22.04

# Labels
LABEL Author="benchmark-prep"
LABEL Description="Container with initial data for line-count benchmark exercise."

RUN set -e && \
    echo "==> Installing Python3 and pytest" && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    echo "==> Creating initial data hierarchy" && \
    mkdir -p /home/user/data/raw/dataset_A && \
    mkdir -p /home/user/data/raw/dataset_B && \
    mkdir -p /home/user/data/raw/dataset_C

# dataset_A - file1.csv
RUN cat > /home/user/data/raw/dataset_A/file1.csv <<'EOF'
id,value
1,a
2,b
3,c
4,d
EOF

# dataset_A - file2.csv
RUN cat > /home/user/data/raw/dataset_A/file2.csv <<'EOF'
id,value
1,e
2,f
3,g
4,h
5,i
6,j
7,k
EOF

# dataset_B - data.csv
RUN cat > /home/user/data/raw/dataset_B/data.csv <<'EOF'
id,amount
1,10
2,20
3,30
4,40
5,50
6,60
7,70
8,80
9,90
EOF

# dataset_C - part1.csv
RUN cat > /home/user/data/raw/dataset_C/part1.csv <<'EOF'
id,sales
1,100
2,150
3,200
EOF

# dataset_C - part2.csv
RUN cat > /home/user/data/raw/dataset_C/part2.csv <<'EOF'
id,sales
1,300
2,350
3,400
4,450
5,500
EOF

# dataset_C - part3.csv
RUN cat > /home/user/data/raw/dataset_C/part3.csv <<'EOF'
id,sales
1,550
2,600
3,650
4,700
5,750
6,800
7,850
8,900
9,950
EOF

RUN echo "==> Setting file permissions" && \
    chmod -R a+rX /home/user && \
    chmod 755 /home/user

WORKDIR /home/user

CMD ["echo", "Container for the benchmark exercise. Execute your commands inside the container as needed."]