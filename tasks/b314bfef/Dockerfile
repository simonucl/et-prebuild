FROM ubuntu:22.04

# Base utilities
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gnupg \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Python testing framework
RUN pip3 install --no-cache-dir pytest

# Create dedicated non-root user and directory skeleton
RUN useradd -m -s /bin/bash user

# Secrets directory
RUN install -d -m 700 /home/user/secrets

RUN cat > /home/user/secrets/db_credentials.txt <<'EOF'
db_user=admin
db_password=Sup3rS3cr3t
EOF

RUN chmod 600 /home/user/secrets/db_credentials.txt

# Incoming directory
RUN install -d -m 755 /home/user/incoming && \
    printf "dummy patch content\n" > /home/user/incoming/patch_v1.tar.gz && \
    chmod 644 /home/user/incoming/patch_v1.tar.gz

RUN cat > /home/user/incoming/patch_v1.tar.gz.asc <<'EOF'
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

dGVzdCBzaWduYXR1cmUK
=abcd
-----END PGP SIGNATURE-----
EOF

RUN chmod 644 /home/user/incoming/patch_v1.tar.gz.asc

# Logs directory
RUN install -d -m 755 /home/user/logs

# Ensure correct ownership
RUN chown -R user:user /home/user

# Set home directory permissions
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8