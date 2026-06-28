FROM ubuntu:24.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

WORKDIR /home/user

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash coreutils findutils gzip tar python3 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user && \
    mkdir -p /home/user/release/src/acme-widget-1.4.2/src/acme_widget \
             /home/user/release/src/acme-widget-1.4.2/config \
             /home/user/release/src/acme-widget-1.4.2/docs \
             /home/user/release/src/acme-widget-1.4.2/scripts \
             /home/user/release/src/acme-widget-1.4.2/build \
             /home/user/release/src/acme-widget-1.4.2/dist \
             /home/user/release/src/acme-widget-1.4.2/.git/objects \
             /home/user/release/src/acme-widget-1.4.2/.pytest_cache && \
    printf '# Acme Widget\n\nSmall command line widget used by release tests.\n' > /home/user/release/src/acme-widget-1.4.2/README.md && \
    printf 'MIT License\n\nCopyright 2024 Acme\n' > /home/user/release/src/acme-widget-1.4.2/LICENSE && \
    printf '[project]\nname = "acme-widget"\nversion = "1.4.2"\nrequires-python = ">=3.10"\n' > /home/user/release/src/acme-widget-1.4.2/pyproject.toml && \
    printf '__version__ = "1.4.2"\n' > /home/user/release/src/acme-widget-1.4.2/src/acme_widget/__init__.py && \
    printf 'def main():\n    print("acme-widget 1.4.2")\n' > /home/user/release/src/acme-widget-1.4.2/src/acme_widget/cli.py && \
    printf '[defaults]\ncolor = "blue"\nretries = 3\n' > /home/user/release/src/acme-widget-1.4.2/config/defaults.toml && \
    printf '2024-01-10: release candidate\n2024-01-17: final release\n' > /home/user/release/src/acme-widget-1.4.2/docs/changelog.md && \
    ln -s changelog.md /home/user/release/src/acme-widget-1.4.2/docs/latest.md && \
    printf '#!/usr/bin/env bash\npython3 -m acme_widget.cli "$@"\n' > /home/user/release/src/acme-widget-1.4.2/scripts/acme-widget && \
    chmod 0755 /home/user/release/src/acme-widget-1.4.2/scripts/acme-widget && \
    printf 'temporary build output\n' > /home/user/release/src/acme-widget-1.4.2/build/generated.bin && \
    printf 'old package\n' > /home/user/release/src/acme-widget-1.4.2/dist/acme-widget-1.4.1.tar.gz && \
    printf 'scratch notes\n' > /home/user/release/src/acme-widget-1.4.2/notes.tmp && \
    printf 'print("debug")\n' > /home/user/release/src/acme-widget-1.4.2/src/acme_widget/debug.tmp && \
    printf 'editor backup\n' > /home/user/release/src/acme-widget-1.4.2/README.md~ && \
    printf '[core]\n\trepositoryformatversion = 0\n' > /home/user/release/src/acme-widget-1.4.2/.git/config && \
    printf 'ref: refs/heads/main\n' > /home/user/release/src/acme-widget-1.4.2/.git/HEAD && \
    printf 'Signature: 8a477f597d28d172789f06886806bc55\n' > /home/user/release/src/acme-widget-1.4.2/.pytest_cache/CACHEDIR.TAG && \
    touch -d '2023-08-02T03:04:05Z' /home/user/release/src/acme-widget-1.4.2/README.md && \
    touch -d '2023-09-03T04:05:06Z' /home/user/release/src/acme-widget-1.4.2/src/acme_widget/cli.py && \
    chown -R user:user /home/user/release

USER user
WORKDIR /home/user
