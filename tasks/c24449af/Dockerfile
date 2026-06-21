# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help: Author account-summary exercise container

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools ca-certificates \
        coreutils grep sed gawk && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/site_admin.log
2024-05-25 09:12:30 useradd alice
2024-05-25 09:15:02 useradd bob
2024-05-25 09:16:45 passwd alice SUCCESS
2024-05-25 09:18:07 passwd alice SUCCESS
2024-05-25 09:20:13 passwd bob FAILURE: password too short
2024-05-25 09:22:50 passwd bob SUCCESS
2024-05-25 09:30:00 userdel dave
2024-05-25 09:35:12 passwd dave FAILURE: user not found
2024-05-25 10:00:00 useradd eve
2024-05-25 10:05:52 passwd eve SUCCESS
EOF

RUN chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/site_admin.log && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:$PATH

CMD echo "This container is prepared for the 'account summary' exercise." && \
    echo "Switch to the 'user' account to begin:  su - user"