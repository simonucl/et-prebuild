#!/bin/bash
set -euo pipefail

ROOT=${TRSI_ROOT:-}
HOME_DIR="$ROOT/home/user"

mkdir -p "$HOME_DIR/.ssh/conf.d" "$HOME_DIR/.ssh/keys"

cat > "$HOME_DIR/.ssh/config" <<'EOF'
Include ~/.ssh/conf.d/*.conf

Host *
    ServerAliveInterval 30
    TCPKeepAlive no
    IdentitiesOnly yes
EOF

cat > "$HOME_DIR/.ssh/conf.d/10-prod.conf" <<'EOF'
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

Host prod-*
    User app
    Port 22
    StrictHostKeyChecking no
EOF

cat > "$HOME_DIR/.ssh/conf.d/20-staging.conf" <<'EOF'
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

cat > "$HOME_DIR/.ssh/conf.d/30-legacy.conf" <<'EOF'
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

chmod 700 "$HOME_DIR/.ssh"
chmod 600 "$HOME_DIR/.ssh/config"
chmod 600 "$HOME_DIR/.ssh/conf.d/"*.conf
chmod 600 "$HOME_DIR/.ssh/keys/"*

summary="$HOME_DIR/.ssh/effective_hosts.tsv"
printf 'alias\thostname\tuser\tport\tproxyjump\tidentityfile\tstricthostkeychecking\n' > "$summary"
for alias in prod-bastion prod-db staging-bastion staging-api legacy-reports; do
  cfg=$(HOME="$HOME_DIR" ssh -F "$HOME_DIR/.ssh/config" -G "$alias")
  get_first() {
    awk -v key="$1" '$1 == key {print substr($0, length($1) + 2); exit}' <<<"$cfg"
  }
  hostname=$(get_first hostname)
  user=$(get_first user)
  port=$(get_first port)
  proxyjump=$(get_first proxyjump)
  identityfile=$(get_first identityfile)
  strict=$(get_first stricthostkeychecking)
  if [[ -z "$proxyjump" || "$proxyjump" == "none" ]]; then
    proxyjump="-"
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$alias" "$hostname" "$user" "$port" "$proxyjump" "$identityfile" "$strict" >> "$summary"
done
chmod 600 "$summary"
