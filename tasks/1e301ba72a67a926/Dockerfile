FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    coreutils \
    findutils \
    python3 \
    unzip \
    zip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN mkdir -p \
    /home/user/tf-mirror-lab/source/provider \
    /home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall \
    /opt/tf-mirror-lab

RUN cat > /home/user/tf-mirror-lab/source/provider/terraform-provider-acmefirewall_v0.4.2 <<'EOF'
#!/bin/sh
set -eu
case "${1:-}" in
  --version)
    printf 'terraform-provider-acmefirewall v0.4.2\n'
    ;;
  *)
    printf 'acme firewall provider offline test binary\n'
    ;;
esac
EOF

RUN cat > /home/user/tf-mirror-lab/source/provider/LICENSE.txt <<'EOF'
Copyright 2026 Acme Corp.

Licensed for internal offline training use only.
EOF

RUN cat > /home/user/tf-mirror-lab/source/provider/README.md <<'EOF'
# Acme Firewall Provider

This note is source-only documentation and must not be included in the provider package.
EOF

RUN chmod 0755 /home/user/tf-mirror-lab/source/provider/terraform-provider-acmefirewall_v0.4.2 \
    && chmod 0644 /home/user/tf-mirror-lab/source/provider/LICENSE.txt \
    && chmod 0644 /home/user/tf-mirror-lab/source/provider/README.md

RUN cat > /home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall/index.json <<'EOF'
{"versions":{"0.4.1":{"protocols":["5.0"],"platforms":[{"os":"linux","arch":"amd64"}]}}}
EOF

RUN cat > /home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall/0.4.2.json <<'EOF'
{"archives":{}}
EOF

RUN printf 'stale zip bytes\n' > /home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall/terraform-provider-acmefirewall_0.4.2_linux_amd64.zip
RUN printf '0000000000000000000000000000000000000000000000000000000000000000  terraform-provider-acmefirewall_0.4.2_linux_amd64.zip\n' > /home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall/SHA256SUMS
RUN printf 'delete me\n' > /home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall/terraform-provider-acmefirewall_0.4.1_linux_amd64.zip

RUN find /home/user/tf-mirror-lab/source/provider -type f -printf '%P\0' \
    | sort -z \
    | xargs -0 -I{} sha256sum "/home/user/tf-mirror-lab/source/provider/{}" \
    | sed 's#/home/user/tf-mirror-lab/source/provider/##' \
    > /opt/tf-mirror-lab/source.sha256

RUN chown -R user:user /home/user/tf-mirror-lab

USER user
WORKDIR /home/user
