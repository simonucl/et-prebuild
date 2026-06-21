# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install Python and pytest
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Prepare project skeleton expected by the tests
# ---------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/project/config && \
    mkdir -p /home/user/project/logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/project && \
    chmod 755 /home/user/project/config && \
    chmod 755 /home/user/project/logs

# ---------------------------------------------------------------------
# Create placeholder configuration files with exact content
# ---------------------------------------------------------------------
RUN cat > /home/user/project/config/cleaning.yml << 'EOF'
remove_duplicates: false
missing_value_strategy: mean
columns: []
EOF

RUN cat > /home/user/project/config/cleaning.toml << 'EOF'
remove_duplicates = false
missing_value_strategy = "mean"
columns = []
EOF

# ---------------------------------------------------------------------
# Set file permissions (0644)
# ---------------------------------------------------------------------
RUN chmod 644 /home/user/project/config/cleaning.yml && \
    chmod 644 /home/user/project/config/cleaning.toml

# Default environment; nothing to override.

# Equivalent of %runscript
CMD ["/bin/bash"]