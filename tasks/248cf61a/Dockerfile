FROM ubuntu:22.04

# Install Python, pip, pytest, locales
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/project/translations && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/project && \
    chmod 0755 /home/user/project/translations

# Create UTF‑8 file via heredoc
RUN cat <<'EOF' > /tmp/messages_de_utf8
greeting=Grüß Gott
farewell=Auf Wiedersehen
thanks=Vielen Dank
EOF

# Convert to ISO‑8859‑1 and move into place
RUN iconv -f UTF-8 -t ISO-8859-1 /tmp/messages_de_utf8 \
      > /home/user/project/translations/messages_de.properties && \
    chmod 0644 /home/user/project/translations/messages_de.properties && \
    rm -f /tmp/messages_de_utf8

# Environment variables
ENV LC_ALL=C.UTF-8

# Default runscript behavior
CMD ["bash"]