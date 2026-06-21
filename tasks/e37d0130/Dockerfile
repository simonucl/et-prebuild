FROM ubuntu:22.04

# Labels
LABEL Author="backup-engineer"
LABEL Description="Container for the finance-data HEAD SHA backup task. Includes pytest and a minimal stubbed Git."

# 1. Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# 2. Create a normal, non-root user "user"
RUN groupadd -g 1000 user && \
    useradd -m -d /home/user -s /bin/bash -u 1000 -g 1000 user

# 3. Set up the required directory hierarchy
RUN install -d -m 0755 /home/user/projects/finance-data && \
    install -d -m 0755 /home/user/backup && \
    install -d -m 0775 /home/user/backup/checks

# 4. Populate files inside the finance-data project - README.md
RUN cat > /home/user/projects/finance-data/README.md <<'EOF'
# Finance Data

Initial dataset.
EOF

# Create minimal .git directory so that tests see "a Git repo"
RUN install -d -m 0755 /home/user/projects/finance-data/.git

# 5. Provide a stubbed "git" executable that satisfies tests
RUN cat > /usr/local/bin/git <<'GITSTUB'
#!/usr/bin/env bash
# Lightweight stub that supports only the commands required by the
# test-harness and student task.

EXPECTED_SHA="7fd1a60b01f91b314f5996f35b385144ae4a9b0f"

# Handle version query (some tools call this).
if [[ "$1" == "--version" ]]; then
    echo "git version 2.34.1 (stub)"
    exit 0
fi

# git rev-parse HEAD
if [[ "$1" == "rev-parse" && "$2" == "HEAD" ]]; then
    echo "${EXPECTED_SHA}"
    exit 0
fi

# git rev-list --count HEAD
if [[ "$1" == "rev-list" && "$2" == "--count" && "$3" == "HEAD" ]]; then
    echo "1"
    exit 0
fi

echo "git stub: unsupported command '$*'" >&2
exit 1
GITSTUB

RUN chmod +x /usr/local/bin/git

# 6. Ensure ownership is correct for the non-root user
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:$PATH
ENV USER=user
ENV HOME=/home/user