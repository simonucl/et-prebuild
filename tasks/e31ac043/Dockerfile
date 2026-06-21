FROM ubuntu:22.04

# Labels
LABEL Author="Integration-Developer Exercise"
LABEL Description="Container for detached-signature verification + symmetric encryption task."

# Set environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install required software
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gnupg \
        python3 \
        python3-pip \
        locales && \
    pip3 install --no-cache-dir pytest && \
    sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create exercise directory structure
RUN mkdir -p /home/user/work/integration

# Create message.txt file
RUN cat > /home/user/work/integration/message.txt <<'EOF'
POST /v1/payments
X-Correlation-ID: 123e4567-e89b-12d3-a456-426614174000
{"amount":42}
EOF

# Generate partner key, export it, sign the message
RUN set -e && \
    export GNUPGHOME=/tmp/integration-gnupg && \
    mkdir -p "${GNUPGHOME}" && \
    chmod 700 "${GNUPGHOME}" && \
    gpg --batch --pinentry-mode loopback --passphrase '' \
        --quick-gen-key "Partner API <partner@example.com>" default default never && \
    gpg --batch --yes -u "Partner API <partner@example.com>" \
        --output /home/user/work/integration/message.txt.sig \
        --detach-sign /home/user/work/integration/message.txt && \
    gpg --armor --output /home/user/work/integration/partner_pub.asc \
        --export "Partner API <partner@example.com>" && \
    rm -rf "${GNUPGHOME}" && \
    chmod 644 /home/user/work/integration/*

# Set permissions on home directory
RUN chmod 755 /home/user

WORKDIR /home/user

# Help information (as comment):
# This container image provides the starting files for the
# "Integration-developer scenario – detached signature verification and
# subsequent symmetric encryption" exercise. Use gpg to import the partner
# key, verify the signature, and then symmetrically encrypt the message as
# described in the assignment.