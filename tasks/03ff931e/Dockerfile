FROM ubuntu:22.04

# Labels
LABEL Author="Container generator"
LABEL Description="Environment for backup verification task with pytest installed"

RUN set -eux && \
    # Install Python and pytest
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    # Create an unprivileged user that mirrors the expected runtime user
    groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true && \
    # Prepare directory structure and files required by the tests
    mkdir -p /home/user/server && \
    mkdir -p /home/user/data && \
    # Create an empty tarball (zero-byte file)
    touch /home/user/data/backup.tar.gz

# Compute SHA-256 hash and generate HTML status page
RUN HASH=$(python3 -c "import hashlib; print(hashlib.sha256(open('/home/user/data/backup.tar.gz', 'rb').read()).hexdigest())") && \
    cat > /home/user/server/backup_report.html <<EOF
<!DOCTYPE html>
<html>
<head><title>Nightly Backup Report</title></head>
<body>
<h1>Backup Verification</h1>
<p>The SHA256 checksum for the latest tarball is: <code>${HASH}</code></p>
</body>
</html>
EOF

# Ensure ownership for the unprivileged user
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user