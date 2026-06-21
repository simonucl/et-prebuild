FROM ubuntu:22.04

# Help section from Apptainer:
# Update APT, install Python, create user, create website files, set environment variables

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN mkdir -p /home/user/my_website/public

RUN cat > /home/user/my_website/public/index.html <<'EOF'
<html><body><h1>Index</h1></body></html>
EOF

RUN cat > /home/user/my_website/public/about.html <<'EOF'
<html><body><h1>About</h1></body></html>
EOF

RUN cat > /home/user/my_website/public/contact.html <<'EOF'
<html><body><h1>Contact</h1></body></html>
EOF

RUN chown -R 1000:1000 /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1