FROM ubuntu:22.04

# Install Python tooling (pytest is required by the grader)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up the initial filesystem state expected by the tests
# Home directory tree
RUN mkdir -p /home/user/infra

# hosts.override with the *old* mappings (must end with exactly one newline)
RUN cat >/home/user/infra/hosts.override <<'EOF'
10.10.10.10 db.internal.example.com
10.10.10.20 api.internal.example.com
10.10.10.30 cache.internal.example.com
EOF

# Non-empty README.txt
RUN echo "Refer to hosts.override for custom hostname mappings (user-controlled hosts file)." \
    >/home/user/infra/README.txt

# Permissions
# Let the non-root runtime user read/write as needed.
RUN chmod 777 /home/user && \
    chmod 777 /home/user/infra && \
    chmod 666 /home/user/infra/hosts.override && \
    chmod 644 /home/user/infra/README.txt

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONUNBUFFERED=1

# Set permissions on startup (note: this runs at build time in Docker)
RUN chmod 755 /home/user