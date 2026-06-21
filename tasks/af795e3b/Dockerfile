FROM ubuntu:22.04

# Install runtime dependencies
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip moreutils parallel && \
    pip3 install --no-cache-dir pytest

# Create baseline filesystem layout
RUN mkdir -p /home/user/releases/1.2.0 && \
    mkdir -p /home/user/releases/1.3.0 && \
    mkdir -p /home/user/releases/2.0.0-beta && \
    mkdir -p /home/user/deployment && \
    chmod 0777 /home/user/deployment

# Populate input files - Version 1.2.0 artifacts
RUN cat > /home/user/releases/1.2.0/artifacts.txt <<'EOF'
app-1.2.0.jar
lib-1.2.0.so
docs-1.2.0.zip
EOF

RUN cat > /home/user/releases/1.2.0/release_notes.txt <<'EOF'
Bug fixes and performance improvements.
EOF

# Populate input files - Version 1.3.0 artifacts
RUN cat > /home/user/releases/1.3.0/artifacts.txt <<'EOF'
app-1.3.0.jar
lib-1.3.0.so
docs-1.3.0.zip
cli-1.3.0.tar.gz
EOF

RUN cat > /home/user/releases/1.3.0/release_notes.txt <<'EOF'
Added new CLI support and minor enhancements.
EOF

# Populate input files - Version 2.0.0-beta artifacts
RUN cat > /home/user/releases/2.0.0-beta/artifacts.txt <<'EOF'
app-2.0.0-beta.jar
lib-2.0.0-beta.so
docs-2.0.0-beta.zip
cli-2.0.0-beta.tar.gz
migrator-2.0.0-beta.sh
EOF

RUN cat > /home/user/releases/2.0.0-beta/release_notes.txt <<'EOF'
Major release beta featuring new architecture overhaul.
EOF

# Set permissive permissions
RUN chmod -R a+rX /home/user/releases && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8