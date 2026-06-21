FROM ubuntu:22.04

# Labels
LABEL Author="devops-task-preparer"
LABEL Description="Environment for version-bump single-command task"

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/service/logs

# Create VERSION file
RUN echo '2.4.1' > /home/user/service/VERSION

# Create CHANGELOG.md via heredoc
RUN cat > /home/user/service/CHANGELOG.md <<'EOF'
# Changelog

## [2.4.1] - 2023-01-15
### Fixed
- Memory leak in worker pool (#1220)

EOF

# Fix permissions
RUN chmod -R 777 /home/user/service

# Commands from %environment requiring execution
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/bin:$PATH"