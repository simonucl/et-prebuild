FROM ubuntu:22.04

# Maintainer="Apptainer Task Setup"

ENV HOME=/home/user

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/incoming

RUN cat > /home/user/expected_release.txt <<'EOF'
core-1.0
util-1.2
gui-3.5
EOF

RUN mkdir -p /tmp/core_pkg && \
    printf 'This is the core artifact\n' > /tmp/core_pkg/core.txt && \
    tar -czf /home/user/incoming/core-1.0.tar.gz -C /tmp/core_pkg core.txt && \
    rm -rf /tmp/core_pkg

RUN mkdir -p /tmp/util_pkg && \
    printf 'This is the util artifact\n' > /tmp/util_pkg/util.txt && \
    tar -czf /home/user/incoming/util-1.2.tar.gz -C /tmp/util_pkg util.txt && \
    rm -rf /tmp/util_pkg

RUN chmod -R a+rwX /home/user