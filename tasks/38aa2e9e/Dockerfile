FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip install --no-cache-dir pytest

# Create seed data directory
RUN mkdir -p /home/user/scan-results && \
    chmod 777 /home/user/scan-results

# Create nmap_output.gnmap file
RUN cat > /home/user/scan-results/nmap_output.gnmap <<'EOF'
# Nmap 7.80 scan initiated
Host: 10.10.0.5 ()  Status: Up
Host: 10.10.0.5 ()  Ports: 21/open/tcp//ftp///, 80/open/tcp//http///, 8080/open/tcp//http-proxy///
Host: 10.10.0.15 () Status: Up
Host: 10.10.0.15 () Ports: 22/open/tcp//ssh///, 139/open/tcp//netbios-ssn///, 445/open/tcp//microsoft-ds///
# Nmap done
EOF

RUN chmod 644 /home/user/scan-results/nmap_output.gnmap

# Create directory for entrypoint script
RUN mkdir -p /docker-entrypoint.d

# Create runtime bootstrap helper script
RUN cat > /docker-entrypoint.d/95-seed-scan-results.sh <<'SEED'
#!/bin/bash
# This script runs at *runtime* to ensure the exercise's initial files
# are present in /home/user even when that directory is bind-mounted from the host.
TARGET_DIR="/home/user/scan-results"
TARGET_FILE="${TARGET_DIR}/nmap_output.gnmap"

if [ ! -f "${TARGET_FILE}" ]; then
    mkdir -p "${TARGET_DIR}"
    chmod 777 "${TARGET_DIR}" || true
    cat > "${TARGET_FILE}" <<'EOF'
# Nmap 7.80 scan initiated
Host: 10.10.0.5 ()  Status: Up
Host: 10.10.0.5 ()  Ports: 21/open/tcp//ftp///, 80/open/tcp//http///, 8080/open/tcp//http-proxy///
Host: 10.10.0.15 () Status: Up
Host: 10.10.0.15 () Ports: 22/open/tcp//ssh///, 139/open/tcp//netbios-ssn///, 445/open/tcp//microsoft-ds///
# Nmap done
EOF
    chmod 644 "${TARGET_FILE}" || true
fi
SEED

RUN chmod 755 /docker-entrypoint.d/95-seed-scan-results.sh

# Create entrypoint script that sources the seed script
RUN cat > /entrypoint.sh <<'ENTRY'
#!/bin/bash
# Run all scripts in /docker-entrypoint.d/
for f in /docker-entrypoint.d/*.sh; do
    if [ -x "$f" ]; then
        . "$f"
    fi
done
exec "$@"
ENTRY

RUN chmod 755 /entrypoint.sh

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user

WORKDIR /home/user

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]