# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help / labels
LABEL Author="Container setup for version-bump task"
LABEL Description="Provides initial state and pytest for automated grading."

# Environment setup (from %environment)
ENV PATH="/home/user/.local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create non-root user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

# Create directories
RUN mkdir -p /home/user/utils

# VERSION file
RUN cat > /home/user/utils/VERSION <<'EOF'
1.4.2
EOF

# CHANGELOG
RUN cat > /home/user/utils/CHANGELOG.md <<'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [1.4.2] - 2023-09-28
### Added
- Initial release of data-parsing utilities.
EOF

# Fix ownership
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user