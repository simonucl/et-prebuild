FROM ubuntu:22.04

# Create a non-root 'user' account with UID/GID 1000 (if not present)
# This matches the typical UID Apptainer will run under so that
# the on-call engineer (student) actually owns the artefacts and can
# modify them without root privileges.
RUN set -e && \
    if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user; \
    fi && \
    if ! getent passwd 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Install Python tooling required for the automated test-harness
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state expected by the tests
RUN mkdir -p /home/user/incident && \
    chmod 755 /home/user/incident

# backup.sh — intentionally world-writable
RUN cat > /home/user/incident/backup.sh <<'EOF'
#!/bin/bash
# Dummy backup script – initial insecure state (world-writable)
echo "Performing backup…"
EOF

RUN chmod 777 /home/user/incident/backup.sh

# .env with the insecure default secret and DB password
RUN cat > /home/user/incident/.env <<'EOF'
SECRET_KEY=INSECURE_DEFAULT
DB_PASSWORD=supersecret
EOF

RUN chmod 644 /home/user/incident/.env

# access.log with at least one probe from 203.0.113.50
RUN cat > /home/user/incident/access.log <<'EOF'
203.0.113.50 - - [17/Aug/2023:14:03:55 +0000] "GET /admin HTTP/1.1" 404 0
192.0.2.10   - - [17/Aug/2023:14:04:00 +0000] "GET /robots.txt HTTP/1.1" 404 0
203.0.113.50 - - [17/Aug/2023:14:04:05 +0000] "GET /wp-login.php HTTP/1.1" 404 0
198.51.100.7 - - [17/Aug/2023:14:04:10 +0000] "GET /login HTTP/1.1" 404 0
203.0.113.50 - - [17/Aug/2023:14:04:15 +0000] "GET /config.php HTTP/1.1" 404 0
EOF

RUN chmod 644 /home/user/incident/access.log

# Give ownership of everything under /home/user to UID/GID 1000
# so the non-root student can work with the files.
RUN chown -R 1000:1000 /home/user

# Set permissions and environment variables
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH