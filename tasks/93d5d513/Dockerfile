FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Prepare initial repository state expected by the automated tests
RUN mkdir -p /home/user/infra-observability

RUN cd /home/user/infra-observability && \
    echo '1.3.4' > VERSION

RUN cd /home/user/infra-observability && \
    cat > package.json <<'EOF'
{
    "name": "infra-observability",
    "version": "1.3.4",
    "private": true,
    "description": "Internal dashboards and alerts"
}
EOF

RUN cd /home/user/infra-observability && \
    cat > CHANGELOG.md <<'EOF'
<!-- Changelog follows keep-a-changelog style -->
## [1.3.4] – 2024-05-22
### Added
- Initial latency dashboard.

EOF

RUN chmod -R a+rwX /home/user/infra-observability && \
    chmod 777 /home/user && \
    chmod 755 /home/user

ENV PATH="$PATH:$HOME/.local/bin"