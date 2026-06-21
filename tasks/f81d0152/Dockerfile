FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        coreutils && \
    python3 -m pip install --no-cache-dir --upgrade pip setuptools && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/support-tool && \
    printf '0.9.7\n' > /home/user/support-tool/VERSION

RUN cat > /home/user/support-tool/CHANGELOG.md <<'EOF'
# Changelog
## [Unreleased]

EOF

RUN chmod -R a+rwX /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8