FROM ubuntu:22.04

# Install required software
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest

# Create non-root user `user`
RUN useradd -m -s /bin/bash user

# Prepare initial remote storage with placeholder files
RUN set -e && \
    REMOTE_BASE=/home/user/remote_storage && \
    mkdir -p "${REMOTE_BASE}/images/dogs" && \
    mkdir -p "${REMOTE_BASE}/images/cats" && \
    mkdir -p "${REMOTE_BASE}/labels" && \
    echo "DOG1_PLACEHOLDER" > "${REMOTE_BASE}/images/dogs/dog1.jpg" && \
    echo "DOG2_PLACEHOLDER" > "${REMOTE_BASE}/images/dogs/dog2.jpg" && \
    echo "CAT1_PLACEHOLDER" > "${REMOTE_BASE}/images/cats/cat1.jpg"

RUN REMOTE_BASE=/home/user/remote_storage && \
cat << 'EOF' > "${REMOTE_BASE}/labels/dog_labels.csv"
id,label
1,bulldog
2,poodle
EOF

RUN REMOTE_BASE=/home/user/remote_storage && \
cat << 'EOF' > "${REMOTE_BASE}/labels/cat_labels.csv"
id,label
1,siamese
2,maine_coon
EOF

# Ensure user owns everything
RUN chown -R user:user /home/user

# Environment setup
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN chmod 755 /home/user

# Labels
LABEL Author="ml-initial-state-preparer"
LABEL Description="Container with initial filesystem state for ML artefact sync task."

CMD ["/bin/bash"]