FROM ubuntu:22.04

# Author On-call Security Engineer
# Description Container prepared for credential-rotation filtering task.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/rotation && \
    chmod 755 /home/user /home/user/rotation

RUN cat > /home/user/rotation/cred_rotation.log <<'EOF'
[2023-11-01 09:13:02] Rotated credential for user alice status=SUCCESS
[2023-11-01 09:15:48] Rotated credential for user bob status=FAIL
[2023-11-01 09:17:31] Rotated credential for user charlie status=SUCCESS
[2023-11-01 09:18:20] Manual update for user dave
[2023-11-02 10:22:11] Rotated credential for user dave status=SUCCESS
[2023-11-02 10:25:46] Rotated credential for user eve status=FAIL
[2023-11-02 10:29:50] Rotated credential for user frank status=SUCCESS
[2023-11-02 10:35:59] Backup completed
[2023-11-02 11:00:01] Rotated credential for user grace status=SUCCESS
EOF

RUN chmod 644 /home/user/rotation/cred_rotation.log