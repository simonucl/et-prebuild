FROM ubuntu:22.04

# --------------------------------------------------------------------- #
# Basic tools                                                           #
# --------------------------------------------------------------------- #
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip rsync && \
    pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Create the initial dataset that the exercise relies on                #
# --------------------------------------------------------------------- #
# Local (source) dataset – five files with exact contents
RUN mkdir -p /home/user/ml_data/raw_dataset/train/images && \
    mkdir -p /home/user/ml_data/raw_dataset/train/labels && \
    mkdir -p /home/user/ml_data/raw_dataset/val/images && \
    mkdir -p /home/user/ml_data/raw_dataset/val/labels

RUN printf 'IMG1\n'    > /home/user/ml_data/raw_dataset/train/images/img1.jpg && \
    printf 'IMG2\n'    > /home/user/ml_data/raw_dataset/train/images/img2.jpg && \
    printf 'label1\n'  > /home/user/ml_data/raw_dataset/train/labels/img1.txt && \
    printf 'IMG3\n'    > /home/user/ml_data/raw_dataset/val/images/img3.jpg && \
    printf 'label3\n'  > /home/user/ml_data/raw_dataset/val/labels/img3.txt

# Remote (staging) dataset – two outdated files only
RUN mkdir -p /home/user/remote_host/staging/dataset/train/images && \
    mkdir -p /home/user/remote_host/staging/dataset/train/labels

RUN printf 'OLD_IMG1\n' > /home/user/remote_host/staging/dataset/train/images/img1.jpg && \
    printf 'oldlbl1\n'  > /home/user/remote_host/staging/dataset/train/labels/img1.txt

# --------------------------------------------------------------------- #
# Permissions: make everything under /home/user writable by the runtime #
# (non-root) user so the agent can modify/sync/delete as needed.        #
# --------------------------------------------------------------------- #
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command
CMD ["/bin/bash"]