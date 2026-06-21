FROM ubuntu:22.04

# Ensure non-interactive APT installs
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y install --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/microservices/auth/logs && \
    mkdir -p /home/user/microservices/payment/logs

# auth/config.yaml
RUN cat <<'EOF' > /home/user/microservices/auth/config.yaml
service_name: auth
version: 1.0.0
port: 8000
database:
  host: localhost
  port: 5432
EOF

# payment/config.yaml
RUN cat <<'EOF' > /home/user/microservices/payment/config.yaml
service_name: payment
version: 1.0.0
port: 8001
database:
  host: localhost
  port: 5432
EOF

# Seed log files
RUN echo "Auth service started at 2024-06-01T00:00:00Z"  > /home/user/microservices/auth/logs/app.log && \
    echo "No errors detected"                            > /home/user/microservices/auth/logs/error.log && \
    echo "Payment service started at 2024-06-01T00:00:00Z" > /home/user/microservices/payment/logs/app.log && \
    echo "No errors detected"                              > /home/user/microservices/payment/logs/error.log

# Permissions
RUN chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Apply chmod from %environment
RUN chmod 755 /home/user