FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/.github/workflows

RUN cat <<'EOF' > /home/user/project/.github/workflows/ci.yml
name: CI
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: '16'
EOF

RUN cat <<'EOF' > /home/user/project/pyproject.toml
[tool.poetry]
name = "demo"
version = "0.1.0"
description = "Demo project"
EOF

RUN chmod -R a+rw /home/user/project

RUN chmod 755 /home/user

CMD echo "Container for CI/CD version-update exercise." && \
    echo "Edit the repository under /home/user/project as per the task instructions."