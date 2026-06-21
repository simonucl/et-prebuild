FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create project directory
RUN mkdir -p /home/user/projects/alpha-tool

# VERSION file
RUN cat <<'EOF' > /home/user/projects/alpha-tool/VERSION
1.2.3
EOF

# CHANGELOG.md
RUN cat <<'EOF' > /home/user/projects/alpha-tool/CHANGELOG.md
# Changelog

## [1.2.0] - 2023-07-07
- Initial public release
EOF

# TODO.md
RUN cat <<'EOF' > /home/user/projects/alpha-tool/TODO.md
- Add support for YAML export
- Refactor config parser
- Improve CLI help text
EOF

# Permissions
RUN chmod -R 777 /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8