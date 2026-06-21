# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update apt index and install Python and pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir --upgrade pytest

# Create user home and project directory
RUN mkdir -p /home/user && \
    mkdir -p /home/user/cloud-migrate

# Create VERSION file
RUN printf '1.2.3\n' > /home/user/cloud-migrate/VERSION

# Create CHANGELOG.md
RUN cat > /home/user/cloud-migrate/CHANGELOG.md <<'EOF'
## [1.2.3] - 2023-09-30
### Added
- Initial deployment pipeline for staging.
EOF

# Ensure log file does not exist
RUN rm -f /home/user/cloud-migrate/version_bump.log

# Permissions for agent
RUN chmod -R 777 /home/user

# Equivalent of %environment PATH update
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH