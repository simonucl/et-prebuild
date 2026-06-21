FROM ubuntu:22.04

# Basic Python tooling for the agent and tests
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the tests
RUN mkdir -p /home/user/artifactmgr

# repos.yaml
RUN cat > /home/user/artifactmgr/repos.yaml <<'EOF'
repositories:
  - name: core-libs
    url: https://artifacts.example.com/core-libs
    type: maven
  - name: dev-tools
    url: https://artifacts.example.com/dev-tools
    type: npm
  - name: graphics
    url: https://artifacts.example.com/graphics
    type: docker
EOF

# settings.toml
RUN cat > /home/user/artifactmgr/settings.toml <<'EOF'
[repository."core-libs"]
autopublish = true

[repository."dev-tools"]
autopublish = false

[repository."graphics"]
autopublish = true
EOF

# Permissions
RUN chmod -R a+rwX /home/user/artifactmgr && \
    chmod 755 /home/user

# Environment
ENV PATH="/root/.local/bin:${PATH}"