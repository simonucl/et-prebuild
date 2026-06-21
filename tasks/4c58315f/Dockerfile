FROM ubuntu:22.04

# Labels
LABEL Author="Container Build Script"
LABEL Description="Environment for the documentation-inventory task"
LABEL Version="1.0"

# Help information as comments
# This container sets up the initial file system state for the
# documentation-inventory automation exercise and provides pytest
# for the embedded grading suite.

# Basic utilities
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a skeleton documentation tree that will be copied to the
# real /home/user/ location at run-time (after $HOME is bind-mounted).
RUN mkdir -p /opt/skel_docs/articles && \
    mkdir -p /opt/skel_docs/tutorials && \
    echo '# Introduction' > /opt/skel_docs/articles/intro.md && \
    echo '# Setup' > /opt/skel_docs/articles/setup.md && \
    echo '# Overview' > /opt/skel_docs/tutorials/overview.md && \
    echo '# Initial site configuration' > /opt/skel_docs/site_config.toml && \
    find /opt/skel_docs -type d -exec chmod 755 {} \; && \
    find /opt/skel_docs -type f -exec chmod 644 {} \;

# Create user and home directory
RUN useradd -m -s /bin/bash user

# Create entrypoint script to provision docs directory at runtime
RUN cat <<'EOF' > /entrypoint.sh
#!/bin/bash
chmod 755 /home/user

# Automatically provision the expected docs directory in /home/user
# the first time the container is executed on a new host system.
DOCS_ROOT="/home/user/docs"

if [ ! -f "${DOCS_ROOT}/articles/intro.md" ]; then
    mkdir -p "${DOCS_ROOT}"
    # Copy skeleton tree created at build time
    cp -R /opt/skel_docs/* "${DOCS_ROOT}/"

    # Give broad rights so the non-root user (the agent) can modify files
    find "${DOCS_ROOT}" -type d -exec chmod 777 {} \;
    find "${DOCS_ROOT}" -type f -exec chmod 666 {} \;
fi

exec "$@"
EOF

RUN chmod +x /entrypoint.sh

ENV HOME=/home/user

WORKDIR /home/user

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]