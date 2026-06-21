FROM ubuntu:22.04

# Labels
LABEL Maintainer="container-builder"
LABEL Description="Environment for documentation version-bump task with initial project state and pytest installed"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the required directory structure and initial files
RUN mkdir -p /home/user/project

# VERSION file with trailing newline
RUN printf "1.2.3\n" > /home/user/project/VERSION

# CHANGELOG.md with exact initial contents (note the blank line after header)
RUN cat <<'EOF' > /home/user/project/CHANGELOG.md
# Changelog

## [1.2.3] - 2023-06-15
### Added
- Initial release of the documentation set.
EOF

# Ensure permissions allow the unprivileged runtime user to modify the files
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PYTHONUTF8=1