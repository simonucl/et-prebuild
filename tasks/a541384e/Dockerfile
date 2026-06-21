FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Exercise="Uptime-dashboard version-bump starter container"

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python testing framework required by the grader
RUN pip3 install --no-cache-dir pytest

# Prepare initial exercise workspace under /home/user
RUN mkdir -p /home/user/uptime-dashboard

WORKDIR /home/user/uptime-dashboard

# 1. VERSION file
RUN echo '1.4.2' > VERSION

# 2. monitor.py with the original (buggy) timeout
RUN cat > monitor.py <<'PY'
"""Simple uptime-monitoring utility (abridged)."""

import time

TIMEOUT = 3  # seconds – intentionally too short (will be fixed later)

def ping(host: str) -> bool:
    """Pretend-ping a host, returning True on success."""
    time.sleep(0.1)  # stand-in for a real network call
    return True
PY

# 3. CHANGELOG.md adhering to Keep a Changelog + SemVer
RUN cat > CHANGELOG.md <<'MD'
# Changelog

## [Unreleased]
### Fixed
- None yet

## [1.4.2] - 2023-11-20
### Added
- Initial uptime monitoring capability.
MD

# Initialise Git repository with a clean working tree
RUN git init -q && \
    git config user.email "sre@example.com" && \
    git config user.name "Site Reliability Engineer" && \
    git add VERSION monitor.py CHANGELOG.md && \
    git commit -q -m "Initial commit: version 1.4.2 with baseline files"

# Ensure every learner will be able to modify the repo (non-root runtime)
RUN chmod -R a+rwX /home/user/uptime-dashboard && \
    chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

# Runscript equivalent
CMD echo "Container for the 'uptime-dashboard' version-bump exercise." && \
    echo "Change directory to /home/user/uptime-dashboard to begin." && \
    exec /bin/bash