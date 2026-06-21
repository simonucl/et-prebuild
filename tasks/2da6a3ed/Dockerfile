FROM ubuntu:22.04

# Help:
# This container provides the initial environment for the
# “Network Diagnostics Bundle” exercise. It includes:
# - A non-root user named “user”
# - Pre-populated /home/user/repositories/targets.list
# - An empty /home/user/artifacts directory
# - Necessary networking tools (ping, traceroute)
# - Python 3 with pytest installed

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        traceroute \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    useradd --create-home --shell /bin/bash --uid 1000 user

RUN set -eux && \
    install -d -m 0755 /home/user/repositories

RUN cat > /home/user/repositories/targets.list <<'EOF'
repo-alpha 127.0.0.1
repo-beta 127.0.0.1
repo-gamma 127.0.0.1
EOF

RUN chmod 0644 /home/user/repositories/targets.list

RUN install -d -m 0755 /home/user/artifacts

RUN chown -R user:user /home/user

RUN chmod 755 /home/user

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin