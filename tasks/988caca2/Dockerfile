FROM ubuntu:22.04

# Author="Apptainer build script for the package-archive exercise"
# Description="Container pre-populated with snapshot data and pytest for autograding."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 1777 /home/user && \
    mkdir -p /home/user/data

RUN cat <<'EOF' >/home/user/data/dpkg_status_snapshot.txt
coreutils 8.32-4.1
bash 5.1-2
grep 3.6-1
dpkg 1.20.9
sed 4.8-1
EOF

RUN chmod 644 /home/user/data/dpkg_status_snapshot.txt && \
    chmod 755 /home/user/data

ENV PATH="$PATH:$HOME/.local/bin"