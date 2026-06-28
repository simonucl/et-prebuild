FROM ubuntu:24.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

WORKDIR /home/user

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      bash \
      ca-certificates \
      openssh-client \
      python3 && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /home/user/.ssh/conf.d /home/user/.ssh/keys; \
    printf '%s\n' \
      'BROKEN PROD KEY - replace only if needed for permissions, not content' \
      > /home/user/.ssh/keys/prod_ed25519; \
    printf '%s\n' \
      'BROKEN STAGING KEY - replace only if needed for permissions, not content' \
      > /home/user/.ssh/keys/staging_ed25519; \
    printf '%s\n' \
      'BROKEN LEGACY KEY - replace only if needed for permissions, not content' \
      > /home/user/.ssh/keys/legacy_rsa; \
    cat > /home/user/.ssh/config <<'EOF'
Host *
    User wrong-default
    ServerAliveInterval 5
    TCPKeepAlive yes
    IdentitiesOnly no

Include ~/.ssh/conf.d/*.conf
EOF
    cat > /home/user/.ssh/conf.d/10-prod.conf <<'EOF'
Host prod-*
    HostName wrong-%h.example.invalid
    User app
    Port 22
    IdentityFile ~/.ssh/keys/staging_ed25519
    StrictHostKeyChecking no

Host prod-bastion
    HostName bastion.prod.internal
    User ops
    Port 2222
    IdentityFile ~/.ssh/keys/prod_ed25519
    StrictHostKeyChecking yes

Host prod-db
    HostName db01.prod.internal
    User postgres
    Port 2222
    ProxyJump prod-bastion
    IdentityFile ~/.ssh/keys/prod_ed25519
    StrictHostKeyChecking yes
    LogLevel ERROR
EOF
    cat > /home/user/.ssh/conf.d/20-staging.conf <<'EOF'
Host staging-bastion
    HostName bastion.staging.internal
    User ops
    Port 2201
    IdentityFile ~/.ssh/keys/staging_ed25519
    StrictHostKeyChecking accept-new

Host staging-api
    HostName api.staging.internal
    User deploy
    Port 2201
    ProxyJump staging-bastion
    IdentityFile ~/.ssh/keys/staging_ed25519
    StrictHostKeyChecking accept-new
EOF
    cat > /home/user/.ssh/conf.d/30-legacy.conf <<'EOF'
Host legacy-reports
    HostName reports.legacy.internal
    User reports
    Port 2200
    IdentityFile ~/.ssh/keys/legacy_rsa
    StrictHostKeyChecking yes
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
    KexAlgorithms +diffie-hellman-group14-sha1
EOF
    chmod 755 /home/user/.ssh; \
    chmod 644 /home/user/.ssh/config /home/user/.ssh/conf.d/*.conf /home/user/.ssh/keys/*

CMD ["bash"]
