FROM ubuntu:22.04

# Author: ChatGPT
# Description: Initial container setup for the “training-data rsync” task

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        rsync && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN mkdir -p /home/user/remote_server/training_data/images && \
    mkdir -p /home/user/remote_server/training_data/labels

RUN cat <<'EOF' >/home/user/remote_server/training_data/images/image1.jpg
fakejpeg1
EOF

RUN cat <<'EOF' >/home/user/remote_server/training_data/images/image2.jpg
fakejpeg22
EOF

RUN cat <<'EOF' >/home/user/remote_server/training_data/labels/image1.txt
label: cat
EOF

RUN cat <<'EOF' >/home/user/remote_server/training_data/labels/image2.txt
label: dog
EOF

RUN cat <<'EOF' >/home/user/remote_server/training_data/README.md
# Demo dataset
EOF

RUN mkdir -p /home/user/local_project

RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH