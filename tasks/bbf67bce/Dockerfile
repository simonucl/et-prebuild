# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install prerequisites
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create initial project structure
RUN mkdir -p /home/user/web_project/css \
    && mkdir -p /home/user/web_project/js \
    && mkdir -p /home/user/web_project/img \
    && mkdir -p /home/user/backups

# index.html
RUN cat > /home/user/web_project/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Demo Site</title>
</head>
<body>
    <h1>Welcome</h1>
</body>
</html>
EOF

# CSS and JS files
RUN echo "body { font-family: Arial, sans-serif; }" > /home/user/web_project/css/style.css
RUN echo "console.log('Hello world');" > /home/user/web_project/js/app.js

# PNG image generation
RUN python3 - << 'PY'
import os, binascii, pathlib
hex_data = (
    "89504e470d0a1a0a0000000d494844520000000100000001"
    "0802000000907753de0000000a4944415478da6364f8ffff"
    "3f0005fe02fe412094070000000049454e44ae426082"
)
path = "/home/user/web_project/img/logo.png"
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "wb") as f:
    f.write(bytes.fromhex(hex_data))
PY

# Permissions
RUN chmod -R a+rwX /home/user \
 && chmod 755 /home/user

ENV PYTHONUNBUFFERED=1