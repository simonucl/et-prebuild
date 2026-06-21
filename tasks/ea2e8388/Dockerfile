FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/my-web-app

RUN cat >/home/user/my-web-app/package.json <<'EOF'
{
  "name": "my-web-app",
  "version": "1.2.3",
  "description": "Sample web app",
  "dependencies": {}
}
EOF

RUN cat >/home/user/my-web-app/CHANGELOG.md <<'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.3] - 2023-07-01
- Initial release.
EOF

RUN chmod -R a+rwX /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8