FROM ubuntu:22.04

# Author sys-hardener-prep
LABEL Author="sys-hardener-prep"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    install -d -m 0755 /home/user/sys-hardener

RUN cat <<'EOF' > /home/user/sys-hardener/config.yaml
version: 1.3.4
hardening:
  ssh:
    permit_root_login: "no"
    password_authentication: "no"
EOF

RUN cat <<'EOF' > /home/user/sys-hardener/CHANGELOG.md
## [1.3.3] - 2023-07-01
### Fixed
- Corrected sysctl typo that prevented IPv6 RA filtering.

## [1.3.2] - 2023-06-10
### Security
- Updated default TLS cipher suite list.
EOF

RUN chown -R user:user /home/user/sys-hardener && chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

USER user