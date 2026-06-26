FROM python:3.12-slim-bookworm

WORKDIR /app

RUN set -eux; \
    mkdir -p /app/provider-src/linux_amd64 /app/provider-src/darwin_arm64; \
    printf '%s\n' '#!/usr/bin/env python3' 'import json' 'print(json.dumps({"provider":"edge-router","version":"1.2.3","platform":"linux_amd64"}, separators=(",", ":")))' > /app/provider-src/linux_amd64/terraform-provider-edge-router_v1.2.3_x5; \
    printf '%s\n' '#!/usr/bin/env python3' 'import json' 'print(json.dumps({"provider":"edge-router","version":"1.2.3","platform":"darwin_arm64"}, separators=(",", ":")))' > /app/provider-src/darwin_arm64/terraform-provider-edge-router_v1.2.3_x5; \
    chmod 0755 /app/provider-src/linux_amd64/terraform-provider-edge-router_v1.2.3_x5 /app/provider-src/darwin_arm64/terraform-provider-edge-router_v1.2.3_x5; \
    mkdir -p /app/mirror/registry.terraform.io/acme/edge-router; \
    printf '{"versions":{"1.2.2":{}}}\n' > /app/mirror/registry.terraform.io/acme/edge-router/index.json; \
    printf '{"archives":{}}\n' > /app/mirror/registry.terraform.io/acme/edge-router/1.2.3.json; \
    printf 'stale archive\n' > /app/mirror/registry.terraform.io/acme/edge-router/terraform-provider-edge-router_1.2.3_linux_amd64.zip; \
    printf 'deadbeef  terraform-provider-edge-router_1.2.3_linux_amd64.zip\n' > /app/mirror/registry.terraform.io/acme/edge-router/SHA256SUMS
