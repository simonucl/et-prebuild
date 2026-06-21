FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Environment for collection-download log cleanup task"

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV DEBIAN_FRONTEND=noninteractive

# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading suite
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create user and directories
RUN useradd -m -s /bin/bash user && \
    mkdir -p /home/user/datasets

# Create the initial download.log with the exact required contents
RUN cat >/home/user/datasets/download.log <<'EOF'
[2023-06-01 10:15:23] OK imagenet_1 152.3MB
[2023-06-01 10:16:05] OK imagenet_2 153.1MB
[2023-06-01 10:16:45] FAIL coco_2017 -
[2023-06-01 10:17:12] OK voc_2012 2.1MB
[2023-06-01 10:18:01] FAIL places365_basic -
[2023-06-01 10:18:34] OK cifar10 0.16MB
[2023-06-01 10:19:10] OK cifar100 0.19MB
[2023-06-01 10:20:22] OK mnist 0.05MB
[2023-06-01 10:21:55] OK fashion_mnist 0.06MB
[2023-06-01 10:22:26] FAIL kitti -
[2023-06-02 09:12:05] OK lsun 34.2MB
[2023-06-02 09:13:11] OK cityscapes 11.3MB
[2023-06-02 09:14:49] OK sun397 23.5MB
[2023-06-02 09:15:30] OK camvid 2.4MB
[2023-06-02 09:16:10] FAIL imagenet21k -
EOF

# Ensure all users can read and write within /home/user
RUN chmod -R 0777 /home/user

# Set up python alias by creating a symlink
RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /home/user

CMD ["echo", "This container sets up the initial state for the collection-download log task. Invoke an interactive shell to work on the exercise."]