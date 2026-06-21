FROM ubuntu:22.04

# Author: mockapi-builder
# Description: Pre-seeded container for the mini-mock API smoke-test assignment.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/mockapi/data && \
    mkdir -p /home/user/mockapi/logs && \
    echo '{"id":101,"username":"testuser","email":"tester@example.com"}' > /home/user/mockapi/data/user.json && \
    echo '{"id":501,"name":"Widget","price":19.99}' > /home/user/mockapi/data/product.json && \
    chmod 755 /home/user

RUN timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ) && \
    cat > /home/user/mockapi/logs/api_test.log <<EOF
TIMESTAMP:${timestamp}
USER_STATUS:000
PRODUCT_STATUS:000
POST_STATUS:000
USERNAME:testuser
PRODUCT_NAME:Widget
EOF

RUN chmod -R a+rX /home/user

LABEL Author="mockapi-builder"
LABEL Description="Pre-seeded container for the mini-mock API smoke-test assignment."