FROM ubuntu:22.04

# Labels
LABEL Author="MachineLearningEngineer"
LABEL Description="Starter image for the packaging-and-verification task."

# Help information (as comments):
# This container provides the initial CSV files in /home/user/raw_data and has
# pytest pre-installed for automated grading.

RUN set -e && \
    echo "Updating package lists and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory structure and CSV data files..." && \
    mkdir -p /home/user/raw_data

RUN cat <<'EOF' > /home/user/raw_data/images_meta.csv
id,height,width
1,256,256
2,128,128
3,512,512
EOF

RUN cat <<'EOF' > /home/user/raw_data/labels.csv
id,label
1,cat
2,dog
3,bird
EOF

RUN cat <<'EOF' > /home/user/raw_data/train_split.csv
id,split
1,train
2,validation
3,test
EOF

RUN chmod -R 755 /home/user && \
    find /home/user/raw_data -type f -exec chmod 644 {} \;

RUN echo "Cleaning up apt caches to reduce image size..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin

WORKDIR /home/user