FROM ubuntu:22.04

# Install Python tooling required for the tests
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up the initial filesystem state expected by the tests
RUN mkdir -p /home/user/stack

RUN cat <<'EOF' > /home/user/stack/compose-auth.yml
services:
  auth-db:
    image: postgres:13
  auth-service:
    image: myregistry/auth-service:1.2.0
EOF

RUN cat <<'EOF' > /home/user/stack/compose-data.yml
services:
  redis:
    image: redis:6-alpine
  data-service:
    image: myregistry/data-service:3.4.5
  auth-db:
    image: postgres:13
EOF

RUN cat <<'EOF' > /home/user/stack/compose-api.yml
services:
  api-gateway:
    image: myregistry/api-gateway:2.0.0
  auth-service:
    image: myregistry/auth-service:1.2.0
EOF

RUN chmod -R a+rX /home/user

# Environment settings
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"