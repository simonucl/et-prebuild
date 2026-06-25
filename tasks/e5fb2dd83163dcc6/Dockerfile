FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    bash \
    bzip2 \
    ca-certificates \
    coreutils \
    python3 \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

WORKDIR /home/user/conda_lab

RUN mkdir -p /home/user/conda_lab/src/acme_tokens /home/user/conda_lab/src/tests /home/user/conda_lab/channel/noarch
RUN printf '%s\n' \
    '__version__ = "0.4.0"' \
    > /home/user/conda_lab/src/acme_tokens/__init__.py
RUN printf '%s\n' \
    'import re' \
    'import sys' \
    'from collections import Counter' \
    '' \
    'TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")' \
    '' \
    'def normalize(text):' \
    '    return [match.group(0).upper().replace("-", "_") for match in TOKEN_RE.finditer(text)]' \
    '' \
    'def main(argv=None):' \
    '    argv = sys.argv[1:] if argv is None else argv' \
    '    text = " ".join(argv) if argv else sys.stdin.read()' \
    '    counts = Counter(normalize(text))' \
    '    for token in sorted(counts):' \
    '        print(f"{token}={counts[token]}")' \
    '' \
    'if __name__ == "__main__":' \
    '    main()' \
    > /home/user/conda_lab/src/acme_tokens/cli.py
RUN printf '%s\n' \
    '# acme-tokens' \
    '' \
    'Small offline tokenizer used by release smoke tests.' \
    > /home/user/conda_lab/src/README.md
RUN printf '%s\n' \
    'MIT License' \
    '' \
    'Copyright 2026 Acme' \
    > /home/user/conda_lab/src/LICENSE
RUN printf '%s\n' \
    'from acme_tokens.cli import normalize' \
    '' \
    'def test_normalize():' \
    '    assert normalize("edge-cache beta") == ["EDGE_CACHE", "BETA"]' \
    > /home/user/conda_lab/src/tests/test_cli.py
RUN printf 'scratch build note\n' > /home/user/conda_lab/src/debug.tmp; \
    printf 'stale package bytes\n' > /home/user/conda_lab/channel/noarch/acme-tokens-0.3.0-py_0.tar.bz2; \
    printf '{"stale":true}\n' > /home/user/conda_lab/channel/noarch/repodata.json; \
    printf '{"stale":true}\n' > /home/user/conda_lab/channel/noarch/current_repodata.json; \
    printf '{"stale":true}\n' > /home/user/conda_lab/channel/channeldata.json; \
    chown -R user:user /home/user/conda_lab

USER user
WORKDIR /home/user/conda_lab
