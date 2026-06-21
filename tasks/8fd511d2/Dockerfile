FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools locales && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create an unprivileged user that the learner will use
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Create directory for exercise data
RUN mkdir -p /home/user/ci_data/commit_authors

# Populate the initial exercise data (author logs) - service-a.log
RUN cat > /home/user/ci_data/commit_authors/service-a.log <<'EOF'
jane.doe@example.com
john.smith@example.com
jane.doe@example.com
alex.lee@example.com
jane.doe@example.com
jane.doe@example.com
john.smith@example.com
jane.doe@example.com
jane.doe@example.com
john.smith@example.com
jane.doe@example.com
EOF

# Populate service-b.log
RUN cat > /home/user/ci_data/commit_authors/service-b.log <<'EOF'
john.smith@example.com
jane.doe@example.com
john.smith@example.com
john.smith@example.com
jane.doe@example.com
jane.doe@example.com
john.smith@example.com
jane.doe@example.com
jane.doe@example.com
EOF

# Populate service-c.log
RUN cat > /home/user/ci_data/commit_authors/service-c.log <<'EOF'
john.smith@example.com
jane.doe@example.com
alex.lee@example.com
john.smith@example.com
john.smith@example.com
jane.doe@example.com
john.smith@example.com
alex.lee@example.com
john.smith@example.com
jane.doe@example.com
EOF

# Ensure correct ownership so the non-root user can access/modify its home
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Set working directory
WORKDIR /home/user

# Default action when the container is run without arguments
CMD ["/bin/bash"]