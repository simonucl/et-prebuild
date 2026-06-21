# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="ChatGPT" \
      Description="Apptainer image for rsync synchronisation task (includes pytest and pre-staged dataset)"

# Install required packages and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip rsync && \
    pip install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create user and home directory
RUN useradd -m -d /home/user user

# Create directory layout expected by the tests
RUN mkdir -p /home/user/remote_dataset && \
    mkdir -p /home/user/ml_project/data && \
    mkdir -p /home/user/ml_project/logs

# Populate the remote dataset with the exact byte-sizes required
RUN cat > /home/user/remote_dataset/train.csv <<'EOF'
id,text,label
1,Hello world,0
2,Another row!,1
3,hey,0
EOF

RUN cat > /home/user/remote_dataset/test.csv <<'EOF'
id,text
1,Hello sync
2,Another!
EOF

RUN cat > /home/user/remote_dataset/README.md <<'EOF'
# Remote Dataset v1
This dataset contains dummy records for sync test.
End.
OK
EOF

# Local placeholder file that must later be removed (27 bytes)
RUN printf 'placeholder to delete soon!' > /home/user/ml_project/data/OLD_FILES_DO_NOT_USE.txt

# Set permissions so the non-root runtime user can read/write
RUN chmod -R 755 /home/user/remote_dataset && \
    chmod -R 777 /home/user/ml_project && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C \
    LANG=C

USER user
WORKDIR /home/user