FROM ubuntu:22.04

# %help: Converted from Apptainer definition

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN chmod 700 /home/user && \
    chmod 700 /home/user/data

RUN cat > /home/user/data/raw_train.tsv <<'EOF'
label	sepal_length	sepal_width	petal_length
Iris-setosa	5.1	3.5	1.4
Iris-versicolor	7.0	3.2	4.7
Iris-virginica	6.3	3.3	6.0
EOF

RUN chmod 644 /home/user/data/raw_train.tsv

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8