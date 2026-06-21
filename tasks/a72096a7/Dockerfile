FROM ubuntu:22.04

# Author BuildArtifactsExercise
# Description Base image with pytest installed and a writable /home/user directory.

LABEL Author="BuildArtifactsExercise" \
      Description="Base image with pytest installed and a writable /home/user directory."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["bash", "-c", "echo 'Container ready. Launch a shell to begin the task.'"]