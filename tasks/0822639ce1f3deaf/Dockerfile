FROM ghcr.io/simonucl/et-envs:69698ccb844b61e0

RUN id user >/dev/null 2>&1 || useradd -m -s /bin/bash user
WORKDIR /app

RUN set -eux; \
    git config --global init.defaultBranch main; \
    rm -rf /home/user/work /home/user/delivery; \
    mkdir -p /home/user/work; \
    chown -R user:user /home/user/work

RUN set -eux; \
    su user -c 'mkdir -p /home/user/work/telemetry-agent && cd /home/user/work/telemetry-agent && git init'; \
    su user -c 'cd /home/user/work/telemetry-agent && git config user.name "Acme Release Bot" && git config user.email "release@example.invalid"'; \
    su user -c 'cd /home/user/work/telemetry-agent && mkdir -p config docs scripts telemetry_agent tests && \
      printf "telemetry-agent 1.7.0\n" > README.md && \
      printf "1.7.0\n" > VERSION && \
      printf "enabled: true\nsample_rate: 0.10\n" > config/default.yaml && \
      printf "#!/usr/bin/env bash\npython3 -m telemetry_agent.cli \"\$@\"\n" > scripts/telemetry-agent && chmod 0755 scripts/telemetry-agent && \
      printf "__version__ = \"1.7.0\"\n" > telemetry_agent/__init__.py && \
      printf "def normalize(event):\n    return {\"kind\": event.get(\"kind\", \"unknown\"), \"value\": event.get(\"value\", 0)}\n" > telemetry_agent/core.py && \
      printf "from .core import normalize\n\ndef main():\n    print(normalize({\"kind\":\"heartbeat\",\"value\":1}))\n" > telemetry_agent/cli.py && \
      printf "base test placeholder\n" > tests/test_core.py && \
      git add README.md VERSION config/default.yaml scripts/telemetry-agent telemetry_agent/__init__.py telemetry_agent/core.py telemetry_agent/cli.py tests/test_core.py && \
      GIT_AUTHOR_DATE="2026-01-10T10:00:00Z" GIT_COMMITTER_DATE="2026-01-10T10:00:00Z" git commit -m "Initialize telemetry agent 1.7.0" && \
      git tag v1.7.0'; \
    su user -c 'cd /home/user/work/telemetry-agent && git checkout -b release/1.7.3 && \
      printf "1.7.3\n" > VERSION && \
      printf "__version__ = \"1.7.3\"\n" > telemetry_agent/__init__.py && \
      git add VERSION telemetry_agent/__init__.py && \
      GIT_AUTHOR_DATE="2026-02-01T09:00:00Z" GIT_COMMITTER_DATE="2026-02-01T09:00:00Z" git commit -m "Bump release version to 1.7.3"'; \
    su user -c 'cd /home/user/work/telemetry-agent && \
      printf "def normalize(event):\n    kind = event.get(\"kind\", \"unknown\").strip().lower().replace(\" \", \"_\")\n    value = int(event.get(\"value\", 0))\n    return {\"kind\": kind, \"value\": value, \"version\": \"1.7.3\"}\n" > telemetry_agent/core.py && \
      git add telemetry_agent/core.py && \
      GIT_AUTHOR_DATE="2026-02-02T09:00:00Z" GIT_COMMITTER_DATE="2026-02-02T09:00:00Z" git commit -m "Normalize event kinds for release"'; \
    su user -c 'cd /home/user/work/telemetry-agent && \
      printf "enabled: true\nsample_rate: 0.25\nredact_headers:\n  - authorization\n  - cookie\n" > config/default.yaml && \
      printf "Release 1.7.3\n=============\n\n- Version bump\n- Event kind normalization\n- Safer default redaction\n" > docs/release-1.7.3.md && \
      git add config/default.yaml docs/release-1.7.3.md && \
      GIT_AUTHOR_DATE="2026-02-03T09:00:00Z" GIT_COMMITTER_DATE="2026-02-03T09:00:00Z" git commit -m "Tighten telemetry defaults" && \
      GIT_AUTHOR_DATE="2026-02-03T09:10:00Z" GIT_COMMITTER_DATE="2026-02-03T09:10:00Z" git tag -a v1.7.3 -m "telemetry-agent 1.7.3"'; \
    su user -c 'cd /home/user/work/telemetry-agent && git checkout main && \
      printf "telemetry-agent 1.8.0-dev\n" > README.md && \
      mkdir -p experiments && printf "batch_size: 500\n" > experiments/batcher.yaml && \
      git add README.md experiments/batcher.yaml && \
      GIT_AUTHOR_DATE="2026-02-04T09:00:00Z" GIT_COMMITTER_DATE="2026-02-04T09:00:00Z" git commit -m "Start 1.8.0 development"'; \
    su user -c 'cd /home/user/work/telemetry-agent && git checkout -b experiment/high-cardinality && \
      mkdir -p experiments && printf "enabled: true\nlimit: 20000\n" > experiments/high-cardinality.yaml && \
      git add experiments/high-cardinality.yaml && \
      GIT_AUTHOR_DATE="2026-02-05T09:00:00Z" GIT_COMMITTER_DATE="2026-02-05T09:00:00Z" git commit -m "Prototype high cardinality metrics"'; \
    su user -c 'cd /home/user/work/telemetry-agent && git checkout release/1.7.3'; \
    su user -c 'git clone --bare /home/user/work/telemetry-agent /home/user/work/receiver.git && cd /home/user/work/receiver.git && \
      git for-each-ref --format="%(refname)" refs/heads refs/tags | grep -v "refs/tags/v1.7.0" | xargs -r -n1 git update-ref -d && \
      git update-ref refs/heads/main refs/tags/v1.7.0 && git symbolic-ref HEAD refs/heads/main'; \
    su user -c 'mkdir -p /home/user/delivery && printf "stale\n" > /home/user/delivery/old-artifact.txt'
