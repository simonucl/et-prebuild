FROM ubuntu:22.04

# OS packages and Python tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pytest

# Create user
RUN useradd -m -s /bin/bash user

# Create log directory
RUN mkdir -p /home/user/app_logs

# serviceA.log
RUN cat > /home/user/app_logs/serviceA.log << 'EOF'
2023-07-01T12:00:00Z 120 200
2023-07-01T12:00:01Z 130 200
2023-07-01T12:00:02Z 125 500
2023-07-01T12:00:03Z 140 200
2023-07-01T12:00:04Z 150 200
2023-07-01T12:00:05Z 110 200
2023-07-01T12:00:06Z 115 200
2023-07-01T12:00:07Z 160 503
2023-07-01T12:00:08Z 135 200
2023-07-01T12:00:09Z 145 200
EOF

# serviceB.log
RUN cat > /home/user/app_logs/serviceB.log << 'EOF'
2023-07-01T12:00:00Z 90 200
2023-07-01T12:00:01Z 95 200
2023-07-01T12:00:02Z 85 200
2023-07-01T12:00:03Z 100 500
2023-07-01T12:00:04Z 92 200
2023-07-01T12:00:05Z 88 200
2023-07-01T12:00:06Z 97 502
2023-07-01T12:00:07Z 89 200
EOF

# Ownership and permissions
RUN chown -R user:user /home/user && chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"