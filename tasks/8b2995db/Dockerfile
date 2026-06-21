FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Exercise Preparation"
LABEL Description="Seeds terraform-module version-bump exercise and installs pytest."

# Help: This container provides the starting state for the terraform-module
# version-bump exercise and includes pytest for automated testing.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir --upgrade pip pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Seed directory structure and initial files
RUN mkdir -p /home/user/terraform-module

# VERSION file
RUN printf '0.4.5\n' > /home/user/terraform-module/VERSION

# CHANGELOG.md with exact initial content
RUN cat > /home/user/terraform-module/CHANGELOG.md <<'EOF'
# Changelog
All notable changes to this project will be documented in this file.

## [0.4.5] - 2023-08-01
### Added
- Initial support for cross-region replication.
EOF

# Ensure non-root users can modify the exercise files
RUN chmod -R a+rwX /home/user