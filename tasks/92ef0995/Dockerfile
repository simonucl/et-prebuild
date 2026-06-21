FROM ubuntu:22.04

# Author certificate-vuln-scan setup
# This container provides the initial filesystem state for the
# certificate vulnerability sweep assignment.
# It contains three certificate dump files in:
#   /home/user/targets/certs
# Pytest is installed so the autograder can run its tests.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p "/home/user/targets/certs"

RUN cat > "/home/user/targets/certs/goodcorp.pem" <<'EOF'
-----BEGIN CERTIFICATE-----
Subject: CN=good.example.com
Signature Algorithm: sha256WithRSAEncryption
Not After : Dec 31 23:59:59 2035 GMT
-----END CERTIFICATE-----
EOF

RUN cat > "/home/user/targets/certs/weakcorp.pem" <<'EOF'
-----BEGIN CERTIFICATE-----
Subject: CN=weak.example.com
Signature Algorithm: sha1WithRSAEncryption
Not After : Dec 31 23:59:59 2035 GMT
-----END CERTIFICATE-----
EOF

RUN cat > "/home/user/targets/certs/oldcorp.pem" <<'EOF'
-----BEGIN CERTIFICATE-----
Subject: CN=expired.example.com
Signature Algorithm: sha256WithRSAEncryption
Not After : Jan  1 00:00:00 2020 GMT
-----END CERTIFICATE-----
EOF

RUN chmod -R 755 /home/user