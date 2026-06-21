FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user
RUN if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -s /bin/bash user; fi

# Create directory tree
RUN mkdir -p /home/user/automation/input

# Seed servers.csv
RUN cat <<'EOF' > /home/user/automation/input/servers.csv
id,name,ip,location
srv01,alpha,10.0.0.1,us-east
srv02,beta,10.0.0.2,us-west
srv03,gamma,10.0.0.3,eu-central
EOF

# Seed metrics.csv
RUN cat <<'EOF' > /home/user/automation/input/metrics.csv
metric_id,server_id,cpu,mem,disk
m001,srv01,55,68,70
m002,srv02,35,40,50
m003,srv03,60,52,80
EOF

# Fix ownership
RUN chown -R 1000:1000 /home/user/automation || true

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Permissions originally in %environment
RUN chmod 755 /home/user

# PATH from %environment
ENV PATH="/home/user/.local/bin:${PATH}"