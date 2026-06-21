# This container sets up the environment for the "Credential Rotation
# Frequency Report" task.
# Inside:
#   /home/user/credentials/rotations.log – the source data
#   A writable /home/user/credentials directory for output
# Use only standard GNU coreutils commands to create rotation_frequency.txt.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/credentials

RUN cat <<'EOF' >/home/user/credentials/rotations.log
alice
bob
charlie
alice
alice
bob
dave
eve
bob
frank
EOF

RUN chmod 0777 /home/user/credentials && \
    chmod 0666 /home/user/credentials/rotations.log && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["/bin/bash"]