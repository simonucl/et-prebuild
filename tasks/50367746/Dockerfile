FROM ubuntu:22.04

# help text
# This container image provides the starting point for the “storage-utils”
# exercise. It installs git, python3, and pytest, and seeds a repository at
# /home/user/storage-utils in the exact initial state expected by the automated
# grader.

LABEL Author="storage-task-preparer"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 777 /home/user

RUN mkdir -p /home/user/storage-utils && chmod 777 /home/user/storage-utils

RUN cat > /home/user/storage-utils/cleanup.sh <<'EOF'
#!/usr/bin/env bash
# Simple placeholder for cleaning /tmp
freed=123
echo "Freed ${freed} MiB"
EOF

RUN chmod 777 /home/user/storage-utils/cleanup.sh

RUN printf "1.2.0\n" > /home/user/storage-utils/VERSION && \
    chmod 666 /home/user/storage-utils/VERSION

RUN cat > /home/user/storage-utils/CHANGELOG.md <<'EOF'
## [1.2.0] - 2023-05-01
### Changed
- Improved file deletion speed.
## [1.1.0] - 2023-04-15
### Added
- Initial cleanup implementation.
EOF

RUN chmod 666 /home/user/storage-utils/CHANGELOG.md

RUN cd /home/user/storage-utils && \
    git init -b main . && \
    git config user.email "builder@example.com" && \
    git config user.name "Builder" && \
    git add cleanup.sh VERSION CHANGELOG.md && \
    git commit -m "chore: initial import 1.2.0"

RUN chmod -R a+rwX /home/user/storage-utils