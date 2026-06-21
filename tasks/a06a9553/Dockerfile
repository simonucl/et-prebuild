# Converted from Apptainer: Bootstrap localimage ./ubuntu_22.04.sif
FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 user && \
    mkdir -p /home/user/storage_sandbox/videos && \
    mkdir -p /home/user/storage_sandbox/docs && \
    truncate -s 10485760 /home/user/storage_sandbox/videos/movie.mp4 && \
    truncate -s 7340032  /home/user/storage_sandbox/docs/archive.zip && \
    truncate -s 5555555  /home/user/storage_sandbox/big_iso.iso && \
    truncate -s 2097152  /home/user/storage_sandbox/videos/short.mov && \
    truncate -s 1024     /home/user/storage_sandbox/docs/notes.txt && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Runscript equivalent
# Default runscript: start a shell as non-root user
CMD ["su", "-", "user"]