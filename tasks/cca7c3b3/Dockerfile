FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/projects/ci_cd/config && \
    chmod -R 0777 /home /home/user /home/user/projects /home/user/projects/ci_cd

RUN cat > /home/user/projects/ci_cd/config/build_settings.ini <<'EOF'
[build]
artifact_name=webapp
timeout=420
retries=3

[runtime]
python_version=3.10
entry_point=app:main

[notifications]
email=devops@example.com
EOF

RUN chmod 0644 /home/user/projects/ci_cd/config/build_settings.ini

ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8