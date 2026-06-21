FROM ubuntu:22.04

# Update package index and install Python + pip.
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the evaluation suite.
RUN pip3 install --no-cache-dir pytest

# Create the initial dataset directory structure and seed files
# exactly as required by the task specification.
RUN mkdir -p /home/user/datasets/coral_reef && \
    chmod 0777 /home/user/datasets/coral_reef

# VERSION file: must contain "1.2.3\n" exactly.
RUN printf "1.2.3\n" > /home/user/datasets/coral_reef/VERSION

# CHANGELOG.md with the precise initial contents.
RUN cat > /home/user/datasets/coral_reef/CHANGELOG.md <<'EOF'
## [1.2.3] - 2023-01-10
### Added
- Added January 2023 reef imagery.

## [1.2.2] - 2022-12-20
### Fixed
- Corrected GPS coordinates.
EOF

# Relax permissions so the non-root user running the container
# can modify these files during the task.
RUN chmod 0666 /home/user/datasets/coral_reef/VERSION \
               /home/user/datasets/coral_reef/CHANGELOG.md

# Set permissions on home directory
RUN chmod 755 /home/user

# Ensure Python user-installed binaries are discoverable.
ENV PATH="/usr/local/bin:${PATH}"