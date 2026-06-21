FROM ubuntu:22.04

# Author: ChatGPT
# Description: Initial environment for the “db-query-opt” release-management task.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db-query-opt

RUN printf "2.4.0\n" > /home/user/db-query-opt/version.txt

RUN cat > /home/user/db-query-opt/CHANGELOG.md <<'EOF'
# Changelog

## [2.4.0] - 2023-04-10
### Added
- Support for composite indexes in query planner

EOF

RUN chmod -R 777 /home/user/db-query-opt

RUN chmod 755 /home/user

ENV PATH="$PATH:/usr/local/bin"