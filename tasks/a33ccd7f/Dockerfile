FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Basic tooling
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Seed data for the required initial state
RUN mkdir -p /opt/initial_state/logs

RUN cat > /opt/initial_state/logs/app.log <<'EOF'
2023-08-21T14:32:07Z ERROR Failed login for user 'admin' from 10.0.0.23
2023-08-21T14:33:58Z INFO User 'alice' authenticated successfully from 10.0.0.11
2023-08-21T14:34:12Z WARN Unauthorized access attempt to /secure/data by user 'bob'
2023-08-21T14:35:47Z ERROR Reflected XSS attempt detected in parameter 'q'
2023-08-21T14:36:02Z DEBUG Cache miss for key 'session_123'
2023-08-21T14:36:15Z INFO User 'alice' logged out
2023-08-21T14:37:00Z WARN Rate limit exceeded for IP 10.0.0.23
EOF

RUN chmod 644 /opt/initial_state/logs/app.log && \
    chmod 755 /opt/initial_state/logs

# Create placeholder /home/user so permissions are correct
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Copy initial state to /home/user/logs
RUN mkdir -p /home/user/logs && \
    cp /opt/initial_state/logs/app.log /home/user/logs/app.log && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/app.log

WORKDIR /home/user

LABEL Author="dev"