FROM ubuntu:22.04

# Help: Container for compressed-backup exercise

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest for the assessment framework..." && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating initial directory structure and draft files..." && \
    mkdir -p /home/user/project_docs

RUN cat >/home/user/project_docs/intro.txt <<'EOF'
Welcome to the intro.
EOF

RUN cat >/home/user/project_docs/usage.txt <<'EOF'
Usage instructions go here.
EOF

RUN cat >/home/user/project_docs/changelog.txt <<'EOF'
Changelog:
* Initial draft completed.
EOF

RUN chmod -R a+rwx /home/user && \
    echo "Container setup for compressed-backup exercise completed."

WORKDIR /home/user

CMD ["/bin/bash", "-c", "echo 'This container is prepared for the compressed-backup exercise.' && echo 'Launch an interactive shell to begin: docker exec -it <container> /bin/bash' && /bin/bash"]