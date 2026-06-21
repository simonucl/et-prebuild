FROM ubuntu:22.04

# Basic tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
RUN mkdir -p /home/user/pipeline_configs/app1 && \
    mkdir -p /home/user/pipeline_configs/app2

# *.tmp files that the agent must rename
RUN cat > /home/user/pipeline_configs/app1/staging.conf.tmp <<'EOF'
# temporary staging configuration
EOF

RUN cat > /home/user/pipeline_configs/app1/prod.conf.tmp <<'EOF'
# temporary production configuration
EOF

RUN cat > /home/user/pipeline_configs/app2/dev.conf.tmp <<'EOF'
# temporary development configuration
EOF

# File that must remain untouched
RUN cat > /home/user/pipeline_configs/app1/settings.conf <<'EOF'
# permanent config – do not touch
EOF

# Permissions
# Give non-root users write access so they can perform the renaming
RUN chmod 777 /home/user && \
    find /home/user/pipeline_configs -type d -exec chmod 777 {} + && \
    find /home/user/pipeline_configs -type f -exec chmod 666 {} +

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Note: chmod 755 /home/user from %environment is moved to an entrypoint or handled at runtime
# For Docker, we set it during build instead
RUN chmod 755 /home/user

CMD ["echo", "Container ready.  Run your commands to complete the renaming task."]