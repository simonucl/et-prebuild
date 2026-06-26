FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    coreutils \
    findutils \
    gzip \
    python3 \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN set -eu; \
    mkdir -p /app/source/edge-filter/src /app/source/edge-filter/debian /app/repo/dists/stable/main/source /app/repo/pool/main/e/edge-filter; \
    printf '%s\n' \
      '# edge-filter' \
      '' \
      'Small deterministic packet filter used by the edge appliance tests.' \
      > /app/source/edge-filter/README.md; \
    printf '%s\n' 'MIT' > /app/source/edge-filter/LICENSE; \
    printf '%s\n' \
      'def normalize_rule(line: str) -> str:' \
      '    return " ".join(line.strip().split()).lower()' \
      '' \
      '' \
      'def accept(rule: str) -> bool:' \
      '    return normalize_rule(rule).startswith("allow ")' \
      > /app/source/edge-filter/src/filter.py; \
    printf '%s\n' \
      'Source: edge-filter' \
      'Section: net' \
      'Priority: optional' \
      'Maintainer: Acme Edge Packaging <packaging@example.invalid>' \
      'Build-Depends: debhelper-compat (= 13), python3' \
      'Standards-Version: 4.7.0' \
      'Homepage: https://example.invalid/edge-filter' \
      'Rules-Requires-Root: no' \
      '' \
      'Package: edge-filter' \
      'Architecture: all' \
      'Depends: ${misc:Depends}, python3' \
      'Description: deterministic edge packet filter helper' \
      ' Small helper library used by edge appliances to normalize packet rules.' \
      > /app/source/edge-filter/debian/control; \
    printf '%s\n' \
      'edge-filter (1.2.0-1) stable; urgency=medium' \
      '' \
      '  * Release deterministic source package for offline repository import.' \
      '' \
      ' -- Acme Edge Packaging <packaging@example.invalid>  Tue, 02 Apr 2024 00:00:00 +0000' \
      > /app/source/edge-filter/debian/changelog; \
    printf '%b\n' '#!/usr/bin/make -f\n%:\n\tdh $@' > /app/source/edge-filter/debian/rules; \
    chmod 0755 /app/source/edge-filter/debian/rules; \
    printf 'stale dsc\n' > /app/repo/pool/main/e/edge-filter/edge-filter_1.1.0-1.dsc; \
    printf 'stale source index\n' > /app/repo/dists/stable/main/source/Sources; \
    printf 'stale compressed index\n' > /app/repo/dists/stable/main/source/Sources.gz; \
    printf 'Origin: stale\n' > /app/repo/dists/stable/Release
