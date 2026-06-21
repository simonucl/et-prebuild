FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem layout and tools required
# for the checksum-verification task (alice, bob, charlie backups). Pytest is
# pre-installed for the automated grading system.

ENV PATH="/home/user/.local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/site_backups && \
    chmod 755 /home/user && \
    chmod 755 /home/user/site_backups && \
    printf 'hello' > /home/user/site_backups/alice.txt && \
    printf 'hello' > /home/user/site_backups/bob.txt && \
    printf 'hello' > /home/user/site_backups/charlie.txt

RUN cat <<'EOF' > /home/user/site_backups/expected_checksums.txt
alice,2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
bob,2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
charlie,2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
EOF

RUN chmod 644 /home/user/site_backups/*.txt