FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      bash \
      ca-certificates \
      coreutils \
      gzip \
      python3 \
      tar && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /home/user/src/widget/src/widget/data \
             /home/user/src/widget/scripts \
             /home/user/src/widget/docs \
             /home/user/src/widget/.git \
             /home/user/src/widget/build \
             /home/user/src/widget/src/widget/__pycache__ \
             /home/user/src/widget/dist; \
    printf '%s\n' \
      '# Widget' \
      '' \
      'Widget is a tiny deterministic packaging sample used by release automation.' \
      > /home/user/src/widget/README.md; \
    printf '%s\n' \
      'MIT License' \
      '' \
      'Copyright (c) 2026 Widget Maintainers' \
      > /home/user/src/widget/LICENSE; \
    printf '%s\n' \
      '[project]' \
      'name = "widget"' \
      'version = "2.4.1"' \
      'requires-python = ">=3.10"' \
      '' \
      '[tool.widget]' \
      'profile = "release"' \
      > /home/user/src/widget/pyproject.toml; \
    printf '%s\n' \
      'VERSION = "2.4.1"' \
      '' \
      'def normalize_name(value: str) -> str:' \
      '    return "-".join(value.strip().lower().split())' \
      > /home/user/src/widget/src/widget/__init__.py; \
    printf '%s\n' \
      'from . import normalize_name' \
      '' \
      'def render_slug(parts):' \
      '    return normalize_name(" ".join(parts))' \
      > /home/user/src/widget/src/widget/core.py; \
    printf '%s\n' \
      '[defaults]' \
      'region = "us-east-1"' \
      'retries = 3' \
      > /home/user/src/widget/src/widget/data/defaults.toml; \
    printf '%s\n' \
      '#!/usr/bin/env bash' \
      'set -euo pipefail' \
      'python3 -c "from widget import normalize_name; print(normalize_name('\''Widget Smoke Test'\''))"' \
      > /home/user/src/widget/scripts/widget-smoke; \
    printf '%s\n' \
      '# Usage' \
      '' \
      'Run scripts/widget-smoke from an environment with src on PYTHONPATH.' \
      > /home/user/src/widget/docs/usage.md; \
    printf '%s\n' '[core]' 'repositoryformatversion = 0' > /home/user/src/widget/.git/config; \
    printf '%s\n' 'transient compiler cache' > /home/user/src/widget/build/cache.tmp; \
    printf 'bytecode placeholder\n' > /home/user/src/widget/src/widget/__pycache__/core.cpython-312.pyc; \
    printf 'old archive placeholder\n' > /home/user/src/widget/dist/widget-2.4.0.tar.gz; \
    chmod 0755 /home/user /home/user/src /home/user/src/widget; \
    find /home/user/src/widget -type d -exec chmod 0755 {} +; \
    find /home/user/src/widget -type f -exec chmod 0644 {} +; \
    chmod 0755 /home/user/src/widget/scripts/widget-smoke; \
    touch -d '2026-05-17T11:22:33Z' /home/user/src/widget/README.md; \
    touch -d '2025-04-01T02:03:04Z' /home/user/src/widget/LICENSE; \
    touch -d '2024-12-25T06:07:08Z' /home/user/src/widget/pyproject.toml; \
    touch -d '2026-01-02T03:04:05Z' /home/user/src/widget/src/widget/__init__.py; \
    touch -d '2026-01-03T04:05:06Z' /home/user/src/widget/src/widget/core.py; \
    touch -d '2026-01-04T05:06:07Z' /home/user/src/widget/src/widget/data/defaults.toml; \
    touch -d '2026-01-05T06:07:08Z' /home/user/src/widget/scripts/widget-smoke; \
    touch -d '2026-01-06T07:08:09Z' /home/user/src/widget/docs/usage.md; \
    rm -rf /home/user/release

CMD ["bash"]
