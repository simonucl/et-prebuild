FROM ubuntu:22.04

# help section not provided in the original

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

RUN cd /home/user && \
    git init incident-tools && \
    cd incident-tools && \
    git checkout -b main && \
    git config user.email "builder@example.com" && \
    git config user.name  "Builder Bot" && \
    echo "1.2.3" > VERSION

RUN cd /home/user/incident-tools && \
    cat > CHANGELOG.md <<'EOF'
## [1.2.3] - 2023-10-02
### Added
- initial release of incident-tools

### Changed
- improved log parsing performance

### Fixed
- corrected typo in README

### Security
- none
EOF

RUN cd /home/user/incident-tools && \
    cat > package.json <<'EOF'
{
  "name": "incident-tools",
  "version": "1.2.3",
  "description": "Internal utilities for incident responders",
  "main": "index.js",
  "license": "MIT"
}
EOF

RUN cd /home/user/incident-tools && \
    git add VERSION CHANGELOG.md package.json && \
    git commit -m "chore: initial 1.2.3 release" && \
    git tag -a v1.2.3 -m "Release 1.2.3"

RUN cd /home/user/incident-tools && \
    echo "// docs update placeholder" > internal.txt && \
    git add internal.txt && \
    git commit -m "docs: update contact escalation path" && \
    echo "// lodash bump" >> internal.txt && \
    git add internal.txt && \
    git commit -m "chore(deps): bump lodash from 4.17.20 to 4.17.21" && \
    echo "// fix null byte handling" >> internal.txt && \
    git add internal.txt && \
    git commit -m "fix(parser): handle null bytes in log stream"

RUN chmod -R a+rwX /home/user/incident-tools && \
    chmod 755 /home/user