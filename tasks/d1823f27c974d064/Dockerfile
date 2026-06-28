FROM cimg/python:3.12.11

WORKDIR /home/circleci

RUN bash --version >/dev/null && \
    python3 --version >/dev/null && \
    git --version >/dev/null && \
    sudo --version >/dev/null && \
    tar --version >/dev/null && \
    gzip --version >/dev/null

RUN set -eux; \
    sudo mkdir -p /solution /tests /logs/verifier; \
    sudo chown -R "$(id -u):$(id -g)" /solution /tests /logs; \
    chmod -R 0777 /solution /tests /logs; \
    mkdir -p /home/circleci/widget-service/src/widget_service \
             /home/circleci/widget-service/scripts \
             /home/circleci/widget-service/tests \
             /home/circleci/widget-service/docs \
             /home/circleci/widget-service/.ci \
             /home/circleci/widget-service/build \
             /home/circleci/releases; \
    cd /home/circleci/widget-service; \
    printf '%s\n' \
      '[project]' \
      'name = "widget-service"' \
      'version = "1.4.2"' \
      'description = "Small internal widget status service"' \
      'requires-python = ">=3.11"' \
      '' \
      '[project.scripts]' \
      'widget-status = "widget_service.cli:main"' \
      > pyproject.toml; \
    printf '%s\n' \
      '# Widget Service' \
      '' \
      'Widget Service reports readiness for the internal widget pipeline.' \
      > README.md; \
    printf '%s\n' \
      '__version__ = "1.4.2"' \
      > src/widget_service/__init__.py; \
    printf '%s\n' \
      'import json' \
      '' \
      '' \
      'def status_payload():' \
      '    return {"service": "widget-service", "status": "ok"}' \
      '' \
      '' \
      'def main():' \
      '    print(json.dumps(status_payload(), separators=(",", ":")))' \
      > src/widget_service/cli.py; \
    printf '%s\n' \
      '#!/usr/bin/env bash' \
      'set -euo pipefail' \
      'python3 -m widget_service.cli >/dev/null' \
      > scripts/healthcheck.sh; \
    chmod 0755 scripts/healthcheck.sh; \
    printf '%s\n' \
      'import widget_service.cli as cli' \
      '' \
      '' \
      'def test_status_payload():' \
      '    assert cli.status_payload()["status"] == "ok"' \
      > tests/test_cli.py; \
    printf '%s\n' \
      '# Draft release notes' \
      '' \
      'These notes are not ready for distribution.' \
      > docs/draft.md; \
    printf '%s\n' \
      'WIDGET_TOKEN=replace-me' \
      > .env.sample; \
    printf '%s\n' \
      'name: release' \
      'on: workflow_dispatch' \
      > .ci/release.yml; \
    printf '%s\n' 'temporary build cache' > build/cache.txt; \
    git init -q; \
    git config user.email "builder@example.invalid"; \
    git config user.name "Image Builder"; \
    git add pyproject.toml README.md src scripts tests docs .env.sample .ci build/cache.txt; \
    git commit -q -m "Initial widget service"; \
    git tag v1.4.2

CMD ["bash"]
