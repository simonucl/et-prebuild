FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends bash python3 ca-certificates coreutils findutils \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/pkg-src/acme_edge_sentinel /app/simple/acme_edge_sentinel /app/simple/acme-edge-sentinel \
 && printf '%s\n' \
'"""ACME edge sentinel package."""' \
'__version__ = "0.6.0"' \
 > /app/pkg-src/acme_edge_sentinel/__init__.py \
 && printf '%s\n' \
'RULES = (' \
'    ("drop", "0.0.0.0/8"),' \
'    ("allow", "10.42.0.0/16"),' \
'    ("audit", "203.0.113.0/24"),' \
')' \
'' \
'def render_rules():' \
'    return "\n".join(f"{action}:{cidr}" for action, cidr in RULES)' \
 > /app/pkg-src/acme_edge_sentinel/rules.py \
 && printf '%s\n' \
'from .rules import render_rules' \
'' \
'def main():' \
'    print(render_rules())' \
'' \
'if __name__ == "__main__":' \
'    main()' \
 > /app/pkg-src/acme_edge_sentinel/cli.py \
 && printf '%s\n' \
'[project]' \
'name = "acme-edge-sentinel"' \
'version = "0.6.0"' \
'requires-python = ">=3.10"' \
'description = "Offline edge policy sentinel"' \
'' \
'[project.scripts]' \
'edge-sentinel = "acme_edge_sentinel.cli:main"' \
 > /app/pkg-src/pyproject.toml \
 && printf '%s\n' \
'stale placeholder' \
 > /app/simple/acme_edge_sentinel/index.html \
 && printf '%s\n' \
'{"name":"acme_edge_sentinel","version":"0.5.9"}' \
 > /app/simple/acme_edge_sentinel/repo-manifest.json \
 && printf '%s\n' \
'<html><body>broken simple index</body></html>' \
 > /app/simple/acme-edge-sentinel/index.html
