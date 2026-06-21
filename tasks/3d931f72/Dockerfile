FROM ubuntu:22.04

# Help / runscript notes
# This container is prepared for the 'archive.test.lan DNS verification' exercise.
# Invoke a shell or execute your commands as needed.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/build/infra

RUN cat <<'EOF' > /home/user/build/infra/hosts_artifacts
# internal artifact hosts mapping
192.168.45.77 archive.test.lan archive
10.8.0.15     artifacts.dev.local dev-artifacts
172.25.11.60  ci-cache.lan cicache

EOF

RUN chmod 0644 /home/user/build/infra/hosts_artifacts && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/build && \
    chmod 0755 /home/user/build/infra && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8