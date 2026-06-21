# Author: observability-dashboard-setup
# Description: Initial state for the version-bump exercise. Pytest pre-installed.
# Help:
# This container provides the starting filesystem state required for the
# “observability-dashboard” version-bump task along with pytest for the
# automated grading suite.

FROM ubuntu:22.04

ENV PATH="$PATH:$HOME/.local/bin"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/observability-dashboard && \
    chmod 777 /home/user && \
    chmod 777 /home/user/observability-dashboard

RUN cat > /home/user/observability-dashboard/VERSION <<'EOF'
1.4.2
EOF

RUN chmod 666 /home/user/observability-dashboard/VERSION

RUN cat > /home/user/observability-dashboard/CHANGELOG.md <<'EOF'
## [1.4.2] - 2023-09-20
### Added
- Initial CPU saturation panel.

EOF

RUN chmod 666 /home/user/observability-dashboard/CHANGELOG.md