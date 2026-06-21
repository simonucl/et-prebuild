FROM ubuntu:22.04

# Help text
# This container provides the initial filesystem and Python/pytest
# environment required for the “artifact-manager” assignment.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/repos/meta

RUN cat > /home/user/repos/meta/core-tools.meta <<'EOF'
a100 core-tools 1.0.0 2048 1111111111111111111111111111111111111111111111111111111111111111
a101 core-tools 1.1.0 1000 2222222222222222222222222222222222222222222222222222222222222222
a102 core-tools 2.0.0 4096 3333333333333333333333333333333333333333333333333333333333333333
EOF

RUN cat > /home/user/repos/meta/core-libs.meta <<'EOF'
b200 core-libs 1.0.0 5120 4444444444444444444444444444444444444444444444444444444444444444
b201 core-libs 1.2.0 500 5555555555555555555555555555555555555555555555555555555555555555
EOF

RUN cat > /home/user/repos/meta/experimental.meta <<'EOF'
x300 experimental 0.1.0 2048 6666666666666666666666666666666666666666666666666666666666666666
EOF

RUN chmod -R a+rX /home/user && chmod 755 /home/user

ENV PYTHON=/usr/bin/python3

CMD ["bash"]