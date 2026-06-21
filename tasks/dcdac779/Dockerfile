FROM ubuntu:22.04

LABEL Author="SingularityTaskBuilder"
LABEL Description="Environment for the Active Users shell-command task with pytest."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/data/users_db

RUN cat >/home/user/data/users_db/passwd.txt <<'EOF'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
alice:x:1000:1000:Alice Admin:/home/alice:/bin/bash
bob:x:1001:1001:Bob Builder:/home/bob:/bin/zsh
charlie:x:1002:1002:Charlie Chaplin:/home/charlie:/bin/bash
dave:x:1003:1003:Dave Developer:/home/dave:/usr/sbin/nologin
erin:x:1004:1004:Erin Example:/home/erin:/bin/bash
EOF

RUN chmod 0777 /home/user

ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

WORKDIR /home/user

CMD ["echo", "Container for the Active Users task. Execute your commands after starting the container."]