# Converted from Apptainer definition file
# Original bootstrap was a local image; using ubuntu:22.04 as the base
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user/webpages && \
    chmod 0777 /home/user

# Create page1.html
RUN cat > /home/user/webpages/page1.html <<'EOF'
<html><head><title>Page One</title></head><body><p>Alpha</p></body></html>
EOF

# Create page2.html
RUN cat > /home/user/webpages/page2.html <<'EOF'
<html><head><title>Page Two</title></head><body><p>Beta</p></body></html>
EOF

# Create page3.html
RUN cat > /home/user/webpages/page3.html <<'EOF'
<html><head><title>Page Three</title></head><body><p>Gamma</p></body></html>
EOF

# Fix permissions
RUN chmod 755 /home/user/webpages && \
    chmod 644 /home/user/webpages/page*.html

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8