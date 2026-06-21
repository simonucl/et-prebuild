FROM ubuntu:22.04

# Install Python tooling (pytest required)
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create project tree
RUN mkdir -p /home/user/projects/website

# package.json
RUN cat >/home/user/projects/website/package.json <<'EOF'
{
  "name": "awesome-website",
  "version": "1.2.3",
  "description": "A demo website",
  "scripts": {
    "start": "node server.js"
  }
}
EOF

# CHANGELOG.md
RUN cat >/home/user/projects/website/CHANGELOG.md <<'EOF'
## [1.2.3] - 2024-05-20
### Fixed
- Resolved navigation bug.
EOF

# Permissions
RUN chmod 0755 /home/user /home/user/projects /home/user/projects/website && \
    chmod 0644 /home/user/projects/website/package.json /home/user/projects/website/CHANGELOG.md

# From %environment section
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin"