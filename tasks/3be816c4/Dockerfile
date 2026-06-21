FROM ubuntu:22.04

# Install runtime dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        file \
        xxd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir pytest

# Prepare initial sandbox state
RUN mkdir -p /home/user/dev_site/pages

# index.html (windows-1252)
RUN cat >/tmp/index_hex <<'EOF'
3c6d65746120636861727365743d2277696e646f77732d31323532223e0a3c68313e4372e86d65204272fb6ce9653c2f68313e0a3c703e50726963653a203130803c2f703e0a
EOF
RUN xxd -r -p /tmp/index_hex >/home/user/dev_site/pages/index.html

# about.html (iso-8859-1)
RUN cat >/tmp/about_hex <<'EOF'
3c6d65746120636861727365743d2269736f2d383835392d31223e0a3c703e5365f16f722061f16f206361f1f36e3c2f703e0a
EOF
RUN xxd -r -p /tmp/about_hex >/home/user/dev_site/pages/about.html

# contact.html (windows-1252)
RUN cat >/tmp/contact_hex <<'EOF'
3c6d65746120636861727365743d2277696e646f77732d31323532223e0a3c703e50686f6e653a202b343920303330203132333435363c2f703e0a3c703e456d61696c3a20fc626572406578616d706c652e636f6d3c2f703e0a
EOF
RUN xxd -r -p /tmp/contact_hex >/home/user/dev_site/pages/contact.html

# Cleanup temporary hex files
RUN rm -f /tmp/index_hex /tmp/about_hex /tmp/contact_hex

# Permissions
RUN chmod 644 /home/user/dev_site/pages/*.html && \
    chmod -R a+rX /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONIOENCODING=utf-8