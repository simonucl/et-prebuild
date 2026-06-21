FROM ubuntu:22.04

# Help: Container prepared for the "semantic version bump & release tagging" task.
# Initial repository is located in /home/user/app.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

RUN mkdir -p /home/user/app

WORKDIR /home/user/app

RUN printf '2.3.4\n' > VERSION

RUN cat > CHANGELOG.md <<'EOF'
## 2.3.4 – 2024-02-10
* Fix: Updated dependency versions.

## 2.3.3 – 2024-02-01
* Change: Improved logging around authentication.
EOF

RUN git init && \
    git config --local user.name "Builder" && \
    git config --local user.email "builder@example.com" && \
    git add VERSION CHANGELOG.md && \
    git commit -m "Initial commit for version 2.3.4" && \
    git tag v2.3.4

RUN chmod -R a+rwX /home/user/app && \
    chmod 755 /home/user

LABEL Author="OpsGenie_AI"