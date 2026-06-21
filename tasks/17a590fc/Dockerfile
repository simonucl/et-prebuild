FROM ubuntu:22.04

# Author "Example Builder"
# Description "Apptainer image for SSH cipher extraction task with pytest installed and initial INI profile present."

ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/sysconfigs

RUN cat > /home/user/sysconfigs/ssh_hardening.ini <<'EOF'
[SSH]
# AllowedCiphers is a comma-separated list.  It may contain extra spaces.
AllowedCiphers = aes256-ctr , aes192-ctr,aes128-ctr , chacha20-poly1305

[RandomUnusedSection]
Foo = bar
EOF

RUN chmod 644 /home/user/sysconfigs/ssh_hardening.ini && \
    chmod 755 /home/user /home/user/sysconfigs || true