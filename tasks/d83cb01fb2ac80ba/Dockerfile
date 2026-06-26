FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    python3 \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/provider-src /app/mirror/registry.acme.test/acme/edgeaudit; \
    printf '%s\n' \
      '#!/bin/sh' \
      'case "$1" in' \
      '  --version)' \
      "    printf '%s\\n' 'terraform-provider-edgeaudit v0.4.2'" \
      '    ;;' \
      '  *)' \
      "    printf '%s\\n' 'edgeaudit provider stub for offline mirror tests'" \
      '    ;;' \
      'esac' \
      > /app/provider-src/terraform-provider-edgeaudit_v0.4.2
RUN chmod 0755 /app/provider-src/terraform-provider-edgeaudit_v0.4.2

RUN set -eux; \
    printf '%s\n' \
      'Apache License' \
      'Version 2.0, January 2004' \
      '' \
      'Copyright 2024 Acme Edge Systems' \
      > /app/provider-src/LICENSE.txt

RUN set -eux; \
    sha256sum /app/provider-src/terraform-provider-edgeaudit_v0.4.2 /app/provider-src/LICENSE.txt > /app/provider-src/SOURCE.sha256; \
    printf '%s\n' '{"versions":{"0.4.1":{},"0.4.2":{"protocols":["5.0"]}}}' > /app/mirror/registry.acme.test/acme/edgeaudit/index.json

RUN set -eux; \
    printf '%s\n' '{"archives":{"linux_amd64":{"url":"terraform-provider-edgeaudit_0.4.1_linux_amd64.zip","hashes":["zh:stale"]}}}' > /app/mirror/registry.acme.test/acme/edgeaudit/0.4.1.json

RUN set -eux; \
    printf 'stale provider bytes\n' > /app/mirror/registry.acme.test/acme/edgeaudit/terraform-provider-edgeaudit_0.4.1_linux_amd64.zip; \
    printf 'wrong platform bytes\n' > /app/mirror/registry.acme.test/acme/edgeaudit/terraform-provider-edgeaudit_0.4.2_darwin_amd64.zip; \
    printf '{"stale":true}\n' > /app/mirror/registry.acme.test/acme/edgeaudit/manifest.json
