FROM ubuntu:22.04

# Author: Data-Management-Task
# Description: Base image for life-science data-management assignment. Pre-populates required CSV datasets and installs pytest.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN set -eux && \
    if ! id -u user > /dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    mkdir -p /home/user/datasets

RUN cat << 'EOF' > /home/user/datasets/experimentsA.csv
sample_id,condition,value
S1,control,0.50
S2,treatment,1.20
S3,treatment,1.10
S4,control,0.45
S5,treatment,1.30
EOF

RUN cat << 'EOF' > /home/user/datasets/experimentsB.csv
sample_id,condition,value
B1,control,0.55
B2,control,0.60
B3,treatment,1.25
B4,treatment,1.15
B5,control,0.58
EOF

RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/datasets

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD /bin/sh -c "echo 'This container provides the baseline environment for the data-management assignment.' && echo 'Open a shell inside the container and follow the instructions given in the exercise.'"