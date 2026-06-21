FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure and initial files
RUN mkdir -p /home/user && \
    mkdir -p /home/user/project && \
    printf "hello" > /home/user/project/app.conf && \
    mkdir -p /home/user/checksums

# Write expected.sha256 using heredoc
RUN cat > /home/user/checksums/expected.sha256 <<'EOF'
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824  app.conf
EOF

# Set safe permissions
RUN chmod 755 /home/user /home/user/project /home/user/checksums && \
    chmod 644 /home/user/project/app.conf /home/user/checksums/expected.sha256

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Labels
LABEL Author="Apptainer Task Preparation Bot"
LABEL Description="Environment for checksum verification assignment"

# Help text
# This container provides the initial file system state required for the
# checksum-verification assignment. pytest is pre-installed for the grader.