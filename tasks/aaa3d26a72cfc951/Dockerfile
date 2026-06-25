FROM ubuntu:24.04

WORKDIR /home/user/vsix_lab

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    python3 \
    unzip \
    zip \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN bash <<'SETUP'
set -euo pipefail
mkdir -p /home/user/vsix_lab/src/extension/syntaxes \
  /home/user/vsix_lab/src/extension/snippets \
  /home/user/vsix_lab/dist
cat > /home/user/vsix_lab/src/extension/package.json <<'EOF'
{
  "name": "acme-log-tools",
  "displayName": "Acme Log Tools",
  "version": "0.8.0",
  "publisher": "acme-corp",
  "engines": {
    "vscode": "^1.92.0"
  },
  "categories": [
    "Other"
  ],
  "contributes": {
    "languages": [
      {
        "id": "acme-log",
        "aliases": [
          "Acme Log",
          "acme-log"
        ],
        "extensions": [
          ".acmelog"
        ],
        "configuration": "./syntaxes/acme-log.tmLanguage.json"
      }
    ]
  }
}
EOF
cat > /home/user/vsix_lab/src/extension/README.md <<'EOF'
# Acme Log Tools

Offline syntax support for Acme service log captures.
EOF
cat > /home/user/vsix_lab/src/extension/LICENSE <<'EOF'
MIT License

Copyright (c) 2026 Acme Corp
EOF
cat > /home/user/vsix_lab/src/extension/syntaxes/acme-log.tmLanguage.json <<'EOF'
{"scopeName":"source.acme-log","patterns":[{"name":"keyword.control.acme-log","match":"\\b(INFO|WARN|ERROR)\\b"},{"name":"constant.numeric.acme-log","match":"\\b[0-9]{3}\\b"}]}
EOF
cat > /home/user/vsix_lab/src/extension/snippets/acme-log.json <<'EOF'
{"Parse request id":{"prefix":"rid","body":["request_id=${1:rid_0000}"],"description":"Insert an Acme request id filter"}}
EOF
cat > /home/user/vsix_lab/src/NOTES.txt <<'EOF'
Release target: 0.9.1
Do not ship NOTES.txt, editor backups, or stale dist artifacts.
EOF
printf 'stale package\n' > /home/user/vsix_lab/dist/acme-log-tools-0.8.0.vsix
printf 'do not keep this file\n' > /home/user/vsix_lab/dist/old-checksums.txt
chown -R user:user /home/user/vsix_lab
SETUP

USER user
