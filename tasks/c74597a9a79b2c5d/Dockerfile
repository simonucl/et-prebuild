FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    python3 \
    unzip \
    zip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN mkdir -p \
      /home/user/wheel_lab/src/acme_ledger_export/schemas \
      /home/user/wheel_lab/dist \
      /home/user/wheel_lab/simple/acme-ledger-export && \
    printf '%s\n' \
      '[project]' \
      'name = "acme-ledger-export"' \
      'version = "0.4.2"' \
      'description = "Offline ledger export normalizer"' \
      'requires-python = ">=3.10"' \
      'dependencies = []' \
      '' \
      '[project.scripts]' \
      'ledger-export = "acme_ledger_export.cli:main"' \
      > /home/user/wheel_lab/src/pyproject.toml && \
    printf '%s\n' \
      '__version__ = "0.4.2"' \
      '' \
      'def normalize_account(value: str) -> str:' \
      '    return value.strip().upper().replace(" ", "-")' \
      > /home/user/wheel_lab/src/acme_ledger_export/__init__.py && \
    printf '%s\n' \
      'from . import normalize_account' \
      '' \
      'def main():' \
      '    print(normalize_account(" cash account "))' \
      '' \
      'if __name__ == "__main__":' \
      '    main()' \
      > /home/user/wheel_lab/src/acme_ledger_export/cli.py && \
    printf '%s\n' \
      '{"type":"object","required":["account","amount"],"properties":{"account":{"type":"string"},"amount":{"type":"number"}}}' \
      > /home/user/wheel_lab/src/acme_ledger_export/schemas/default.json && \
    printf '%s\n' 'temporary editor backup - do not package' > /home/user/wheel_lab/src/acme_ledger_export/cli.py~ && \
    printf '%s\n' 'scratch notes - do not package' > /home/user/wheel_lab/src/NOTES.tmp && \
    printf '%s\n' 'old broken wheel placeholder' > /home/user/wheel_lab/dist/acme_ledger_export-0.4.2-py3-none-any.whl && \
    printf '%s\n' '0000000000000000000000000000000000000000000000000000000000000000  acme_ledger_export-0.4.2-py3-none-any.whl' > /home/user/wheel_lab/dist/SHA256SUMS && \
    printf '%s\n' '<html><body>stale index</body></html>' > /home/user/wheel_lab/simple/acme-ledger-export/index.html && \
    chown -R user:user /home/user/wheel_lab

USER user
WORKDIR /home/user
