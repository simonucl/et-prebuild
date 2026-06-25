FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates coreutils file python3 unzip zip \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/provider-src/linux_amd64 /app/provider-src/linux_arm64 /app/mirror/registry.terraform.io/acme/edgecache; \
    printf '%s\n' '#!/bin/sh' 'echo edgecache provider linux_amd64 v1.2.0' > /app/provider-src/linux_amd64/terraform-provider-edgecache_v1.2.0_x5; \
    printf '%s\n' '#!/bin/sh' 'echo edgecache provider linux_arm64 v1.2.0' > /app/provider-src/linux_arm64/terraform-provider-edgecache_v1.2.0_x5; \
    chmod 0755 /app/provider-src/linux_amd64/terraform-provider-edgecache_v1.2.0_x5 /app/provider-src/linux_arm64/terraform-provider-edgecache_v1.2.0_x5; \
    printf '%s\n' 'EdgeCache Provider' 'Offline training fixture for Terraform mirror repair.' > /app/provider-src/README.md; \
    printf '%s\n' 'Copyright 2026 Acme Corp.' 'SPDX-License-Identifier: Apache-2.0' > /app/provider-src/LICENSE.txt; \
    printf '%s\n' '{"versions":{"1.2.0":{"broken":true}}}' > /app/mirror/registry.terraform.io/acme/edgecache/index.json; \
    printf '%s\n' '{"archives":{}}' > /app/mirror/registry.terraform.io/acme/edgecache/1.2.0.json; \
    printf 'stale artifact\n' > /app/mirror/registry.terraform.io/acme/edgecache/terraform-provider-edgecache_1.2.0_linux_amd64.zip; \
    printf 'stale artifact\n' > /app/mirror/registry.terraform.io/acme/edgecache/terraform-provider-edgecache_1.2.0_linux_arm64.zip
