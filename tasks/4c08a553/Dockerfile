# Author TaskSetup
# Description "Initial state for credential rotation parsing challenge"

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/rotation && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/rotation

RUN cat > /home/user/rotation/credential_rotation.log <<'EOF'
[2024-05-03 09:14:02] user=alice action=update password_old=2c1743a password_new=10ac5bd
[2024-05-03 09:15:45] user=alice action=confirm rotation_status=success
[2024-05-03 10:01:11] user=bob action=update password_old=ffab23a password_new=946adfe
[2024-05-03 10:03:02] user=bob action=confirm rotation_status=success
[2024-05-03 11:20:55] user=charlie action=update password_old=ab41dfe password_new=dfee551
[2024-05-03 11:22:11] user=charlie action=confirm rotation_status=success
[2024-05-03 12:10:13] user=david action=confirm rotation_status=success
EOF

RUN chmod 0666 /home/user/rotation/credential_rotation.log

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN chmod 755 /home/user

CMD echo "Container for credential rotation parsing challenge." && \
    echo "Open a shell with:  docker run -it <image> /bin/bash"