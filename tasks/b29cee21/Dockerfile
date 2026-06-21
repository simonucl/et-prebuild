FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare the initial exercise filesystem under /home/user
RUN mkdir -p /home/user/workspace/project/utils && \
    mkdir -p /home/user/remote_host/project_backup

# Source-project files
RUN cat >/home/user/workspace/project/app.py <<'EOF'
print('Hello World')
EOF

RUN cat >/home/user/workspace/project/config.yaml <<'EOF'
env: dev
EOF

RUN cat >/home/user/workspace/project/secrets.yaml <<'EOF'
password: hunter2
EOF

RUN cat >/home/user/workspace/project/notes.tmp <<'EOF'
scratch
EOF

RUN cat >/home/user/workspace/project/README.md <<'EOF'
# Demo Project
EOF

RUN cat >/home/user/workspace/project/utils/helper.py <<'EOF'
def helper():
    return 'helper'
EOF

# Permissions: allow the unprivileged runtime user full access
RUN chmod -R 0777 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user