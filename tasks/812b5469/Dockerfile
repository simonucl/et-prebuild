FROM ubuntu:22.04

# Help: This container image sets up the initial filesystem state required for
# the credential-rotation exercise and includes pytest for automated
# validation.

RUN set -e && \
    apt-get update && \
    apt-get -y install python3-pip curl lynx w3m && \
    pip3 install --no-cache-dir pytest

# Create base user directory
RUN mkdir -p /home/user

# 1) /home/user/portal/ with exactly one file: rotation.html
RUN mkdir -p /home/user/portal

RUN cat > /home/user/portal/rotation.html <<'EOF'
<!DOCTYPE html>
<html>
<head><title>API Token Rotation</title></head>
<body>
<p>New API token for portal integration:</p>
<code id="api-token">SECURETOKEN12345</code>
</body>
</html>
EOF

# 2) /home/user/credentials/ directory, intentionally empty but writable
RUN mkdir -p /home/user/credentials

# Permissions
# Allow any unprivileged container user to read portal contents and
# write into credentials.
RUN chmod 755 /home/user && \
    chmod 755 /home/user/portal && \
    chmod 644 /home/user/portal/rotation.html && \
    chmod 777 /home/user/credentials

LABEL Author="Apptainer Task Setup"