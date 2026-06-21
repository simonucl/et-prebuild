FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial project layout
RUN mkdir -p /home/user/websvc/incidents

# package.json
RUN cat <<'EOF' > /home/user/websvc/package.json
{
  "name": "websvc",
  "version": "2.5.3",
  "description": "Example microservice",
  "main": "index.js"
}
EOF

# CHANGELOG.md
RUN cat <<'EOF' > /home/user/websvc/CHANGELOG.md
## [2.5.3] - 2024-04-07
### Added
- Introduce tracing headers

## [2.5.2] - 2024-03-11
### Fixed
- Patch dependency vulnerabilities
EOF

# Placeholder incident report
RUN touch /home/user/websvc/incidents/2024-05-17_cpu_spike.txt

# Ensure writable home
RUN chmod -R a+rwX /home/user

# Labels (non-command content preserved as comments)
# chmod 755 /home/user
LABEL Author="setup-script"
LABEL Description="Apptainer image for semantic version bump task"

# Environment section (none defined)
# No overrides; retain caller's $HOME