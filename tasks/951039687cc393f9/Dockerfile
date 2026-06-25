FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    findutils \
    git \
    gzip \
    python3 \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

WORKDIR /home/user/archive_lab

RUN set -eux; \
    mkdir -p repo/src/ledger_agent repo/dist repo/scratch out; \
    cd repo; \
    git init -q; \
    git config user.name "Release Bot"; \
    git config user.email "release-bot@example.invalid"; \
    printf 'ledger-agent\n============\n\nRelease: 2.1.0\nRevision: $Format:%%H$\n' > README.md; \
    printf '2.1.0\n' > VERSION; \
    printf '[project]\nname = "ledger-agent"\nversion = "2.1.0"\ndescription = "offline ledger summarizer"\nrequires-python = ">=3.10"\n' > pyproject.toml; \
    printf '"""Ledger agent package."""\n__version__ = "2.1.0"\n' > src/ledger_agent/__init__.py; \
    printf 'def main():\n    print("ledger-agent 2.1.0")\n\nif __name__ == "__main__":\n    main()\n' > src/ledger_agent/cli.py; \
    printf '/dist export-ignore\n/scratch export-ignore\n*.tmp export-ignore\nREADME.md export-subst\n' > .gitattributes; \
    printf 'do not ship\n' > scratch/debug.tmp; \
    printf 'old build\n' > dist/old-wheel.txt; \
    git add README.md VERSION pyproject.toml src .gitattributes scratch/debug.tmp dist/old-wheel.txt; \
    GIT_AUTHOR_DATE='2026-04-12T09:30:00+00:00' GIT_COMMITTER_DATE='2026-04-12T09:30:00+00:00' git commit -q -m 'release ledger-agent 2.1.0'; \
    GIT_COMMITTER_DATE='2026-04-12T09:31:00+00:00' git tag -a v2.1.0 -m 'ledger-agent 2.1.0'; \
    printf 'stale artifact\n' > /home/user/archive_lab/out/ledger-agent-2.1.0.tar.gz; \
    printf 'stale checksum\n' > /home/user/archive_lab/out/ledger-agent-2.1.0.tar.gz.sha256; \
    printf '{"status":"stale"}\n' > /home/user/archive_lab/out/manifest.json; \
    printf 'remove me\n' > /home/user/archive_lab/out/notes.txt; \
    chown -R user:user /home/user/archive_lab

USER user
WORKDIR /home/user/archive_lab
