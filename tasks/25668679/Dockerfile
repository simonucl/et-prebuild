FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user 'user' (UID/GID 1000)
RUN set -e && \
    if ! getent group 1000 >/dev/null 2>&1; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 user; fi

# Prepare initial workspace
RUN mkdir -p /home/user/hardening && \
    chmod 0755 /home/user/hardening

RUN cat > /home/user/hardening/tuned.conf <<'EOF'
# Kernel scheduler settings
sched_migration_cost_ns = 500000
sched_latency_ns = 6000000
sched_min_granularity_ns = 750000
# end
EOF

RUN chmod 0644 /home/user/hardening/tuned.conf && \
    chown -R 1000:1000 /home/user || true && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"