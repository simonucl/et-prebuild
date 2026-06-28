#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=1

fail() {
  echo "FAIL: $*" >&2
  reward=0
}

ROOT=${TRSI_ROOT:-}
HOME_DIR="$ROOT/home/user"
CFG="$HOME_DIR/.ssh/config"

mode_is() {
  local path=$1
  local expected=$2
  local actual
  actual=$(stat -c '%a' "$path" 2>/dev/null) || {
    fail "missing path for mode check: $path"
    return
  }
  [[ "$actual" == "$expected" ]] || fail "$path mode is $actual, expected $expected"
}

first_value() {
  local alias=$1
  local key=$2
  HOME="$HOME_DIR" ssh -F "$CFG" -G "$alias" 2>/dev/null | awk -v key="$key" '$1 == key {print substr($0, length($1) + 2); exit}'
}

expect_value() {
  local alias=$1
  local key=$2
  local expected=$3
  local actual
  actual=$(first_value "$alias" "$key")
  [[ "$actual" == "$expected" ]] || fail "$alias $key is '$actual', expected '$expected'"
}

expect_contains_token() {
  local alias=$1
  local key=$2
  local token=$3
  local actual
  actual=$(first_value "$alias" "$key")
  [[ "$actual" == *"$token"* ]] || fail "$alias $key does not contain $token; actual '$actual'"
}

[[ -f "$CFG" ]] || fail "missing $CFG"
if [[ -f "$CFG" ]]; then
  HOME="$HOME_DIR" ssh -F "$CFG" -G prod-db >/tmp/prod-db.effective 2>/tmp/ssh-g.err || fail "ssh -G cannot parse repaired config"
fi

mode_is "$HOME_DIR/.ssh" 700
mode_is "$CFG" 600
for path in "$HOME_DIR"/.ssh/conf.d/*.conf "$HOME_DIR"/.ssh/keys/*; do
  [[ -e "$path" ]] && mode_is "$path" 600
done

for alias in prod-bastion prod-db staging-bastion staging-api legacy-reports; do
  expect_value "$alias" serveraliveinterval 30
  expect_value "$alias" tcpkeepalive no
  expect_value "$alias" identitiesonly yes
done

expect_value prod-bastion hostname bastion.prod.internal
expect_value prod-bastion user ops
expect_value prod-bastion port 2222
expect_value prod-bastion identityfile "~/.ssh/keys/prod_ed25519"
expect_value prod-bastion stricthostkeychecking true

expect_value prod-db hostname db01.prod.internal
expect_value prod-db user postgres
expect_value prod-db port 2222
expect_value prod-db proxyjump prod-bastion
expect_value prod-db identityfile "~/.ssh/keys/prod_ed25519"
expect_value prod-db stricthostkeychecking true

expect_value staging-bastion hostname bastion.staging.internal
expect_value staging-bastion user ops
expect_value staging-bastion port 2201
expect_value staging-bastion identityfile "~/.ssh/keys/staging_ed25519"
expect_value staging-bastion stricthostkeychecking accept-new

expect_value staging-api hostname api.staging.internal
expect_value staging-api user deploy
expect_value staging-api port 2201
expect_value staging-api proxyjump staging-bastion
expect_value staging-api identityfile "~/.ssh/keys/staging_ed25519"
expect_value staging-api stricthostkeychecking accept-new

expect_value legacy-reports hostname reports.legacy.internal
expect_value legacy-reports user reports
expect_value legacy-reports port 2200
expect_value legacy-reports identityfile "~/.ssh/keys/legacy_rsa"
expect_value legacy-reports stricthostkeychecking true
expect_contains_token legacy-reports hostkeyalgorithms ssh-rsa
expect_contains_token legacy-reports pubkeyacceptedalgorithms ssh-rsa
expect_contains_token legacy-reports kexalgorithms diffie-hellman-group14-sha1

expected=$(mktemp)
cat > "$expected" <<'EOF'
alias	hostname	user	port	proxyjump	identityfile	stricthostkeychecking
EOF
{
  printf 'prod-bastion\tbastion.prod.internal\tops\t2222\t-\t~/.ssh/keys/prod_ed25519\ttrue\n'
  printf 'prod-db\tdb01.prod.internal\tpostgres\t2222\tprod-bastion\t~/.ssh/keys/prod_ed25519\ttrue\n'
  printf 'staging-bastion\tbastion.staging.internal\tops\t2201\t-\t~/.ssh/keys/staging_ed25519\taccept-new\n'
  printf 'staging-api\tapi.staging.internal\tdeploy\t2201\tstaging-bastion\t~/.ssh/keys/staging_ed25519\taccept-new\n'
  printf 'legacy-reports\treports.legacy.internal\treports\t2200\t-\t~/.ssh/keys/legacy_rsa\ttrue\n'
} >> "$expected"

if [[ ! -f "$HOME_DIR/.ssh/effective_hosts.tsv" ]]; then
  fail "missing effective_hosts.tsv"
elif ! diff -u "$expected" "$HOME_DIR/.ssh/effective_hosts.tsv" >&2; then
  fail "effective_hosts.tsv content mismatch"
fi
rm -f "$expected"

echo "$reward" > /logs/verifier/reward.txt
exit 0
