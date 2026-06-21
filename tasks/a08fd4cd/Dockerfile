FROM ubuntu:22.04

# Author "Generated for the Python-file catalogue exercise"
# Description "Ubuntu 22.04 base with pytest installed and initial webapp source tree present."

RUN set -e && \
    echo ">> Updating APT package index and installing Python/pip ..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo ">> Installing pytest for the evaluation test-suite ..." && \
    pip3 install --no-cache-dir pytest

RUN echo ">> Preparing initial project directory tree and source files ..." && \
    mkdir -p /home/user/projects/webapp/src/utils

RUN cat <<'EOF' > /home/user/projects/webapp/src/app.py
print('Hello World')
EOF

RUN cat <<'EOF' > /home/user/projects/webapp/src/config.py
DEBUG = True
EOF

RUN cat <<'EOF' > /home/user/projects/webapp/src/utils/helpers.py
def add(a, b):
    return a + b
EOF

RUN chmod -R a+rwX /home/user

RUN chmod 755 /home/user

ENV PATH="$PATH:/home/user/.local/bin"