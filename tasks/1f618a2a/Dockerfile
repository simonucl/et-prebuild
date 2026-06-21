FROM ubuntu:22.04

# Help / labels
# Author: compliance-task-prep
# Description: Initial state container for certificate compliance audit exercise

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/certs

RUN cat <<'EOF' > /home/user/certs/website_valid.pem
-----BEGIN CERTIFICATE-----
notAfter=Nov 12 12:00:00 2031 GMT
EOF

RUN cat <<'EOF' > /home/user/certs/old_service.pem
-----BEGIN CERTIFICATE-----
notAfter=Jan  1 00:00:00 2021 GMT
EOF

RUN chmod 644 /home/user/certs/*.pem && \
    chmod 777 /home/user /home/user/certs && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH