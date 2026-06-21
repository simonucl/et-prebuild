# Author: exercise-preparer
# Description: Container image for user-account management exercise

FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat <<'EOF' > /home/user/legacy_users.tmp
old_alpha
old_beta
old_gamma
EOF

RUN chmod 0666 /home/user/legacy_users.tmp

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1

CMD echo "Container for account-management exercise. Use an interactive shell to begin."