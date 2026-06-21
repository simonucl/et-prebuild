FROM ubuntu:22.04

# Help text
# This container provides the initial filesystem state required for the
# “API log aggregation” exercise. It includes pytest for automated verification.

# System packages
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip

# Python testing framework
RUN pip3 install --no-cache-dir pytest

# Directory structure
RUN mkdir -p /home/user/api_tests

# Populate api1.log
RUN cat <<'EOF' > /home/user/api_tests/api1.log
2023-07-01T12:00:00Z ERROR 500 INTERNAL_SERVER_ERROR /v1/users/123
2023-07-01T12:00:02Z INFO 204 NO_CONTENT /v1/users/123
EOF

# Populate api2.log
RUN cat <<'EOF' > /home/user/api_tests/api2.log
2023-07-02T15:30:10Z ERROR 504 GATEWAY_TIMEOUT /v1/orders
2023-07-02T15:31:10Z INFO 201 CREATED /v1/orders
EOF

# Populate deprecated.log
RUN cat <<'EOF' > /home/user/api_tests/deprecated.log
2023-06-30T10:00:00Z ERROR 410 GONE /v0/legacy
EOF

# Permissions
RUN chmod 1777 /home/user/api_tests && \
    chmod 0644 /home/user/api_tests/*.log

LABEL Author="integration-test-fixture"