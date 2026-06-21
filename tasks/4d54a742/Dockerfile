FROM ubuntu:22.04

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem state
RUN mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/source_data

RUN cat > /home/user/source_data/iris.csv <<'EOF'
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
7.0,3.2,4.7,1.4,versicolor
6.3,3.3,6.0,2.5,virginica
EOF

RUN chmod 644 /home/user/source_data/iris.csv && \
    chmod 755 /home/user/source_data

ENV LC_ALL=C
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Default command
CMD ["/bin/bash"]