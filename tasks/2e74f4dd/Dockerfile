FROM ubuntu:22.04

# Help section from Apptainer (none provided)

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/certs/input

RUN cat >/home/user/certs/input/example_root.pem <<'EOF'
-----BEGIN CERTIFICATE-----
Subject=CN=Example Root CA
Issuer=CN=Example Root CA
NotBefore=2020-01-01 00:00:00
NotAfter=2020-01-31 00:00:00
-----END CERTIFICATE-----
EOF

RUN cat >/home/user/certs/input/www_acme_com.pem <<'EOF'
-----BEGIN CERTIFICATE-----
Subject=CN=www.acme.com
Issuer=CN=Example Root CA
NotBefore=2021-06-01 00:00:00
NotAfter=2021-12-01 00:00:00
-----END CERTIFICATE-----
EOF

RUN cat >/home/user/certs/input/expired_test.pem <<'EOF'
-----BEGIN CERTIFICATE-----
Subject=CN=expired.example.com
Issuer=CN=Example Root CA
NotBefore=2019-01-01 00:00:00
NotAfter=2019-01-15 00:00:00
-----END CERTIFICATE-----
EOF

RUN chmod 755 /home /home/user /home/user/certs /home/user/certs/input && \
    chmod 644 /home/user/certs/input/*.pem

RUN rm -rf /home/user/cert_diagnostics || true