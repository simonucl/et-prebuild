#!/bin/bash
set -u

mkdir -p /logs/verifier
ROOT=/home/user/unitroot
DROPIN_DIR="$ROOT/etc/systemd/system/ledger-ingest.service.d"
DROPIN="$DROPIN_DIR/20-offline-hardening.conf"
ENVFILE="$ROOT/etc/ledger-ingest/worker.env"
CONFIG="$ROOT/etc/ledger-ingest/config.yaml"
SYSUSERS="$ROOT/etc/sysusers.d/ledger-ingest.conf"
TMPFILES="$ROOT/etc/tmpfiles.d/ledger-ingest.conf"
MANIFEST="$ROOT/etc/ledger-ingest/deployment-manifest.json"

fail() {
  echo "FAIL: $1"
  echo 0 > /logs/verifier/reward.txt
  exit 0
}

mode_of() {
  stat -c '%a' "$1" 2>/dev/null
}

owner_group_of() {
  stat -c '%u:%g' "$1" 2>/dev/null
}

assert_file_exact() {
  local path="$1"
  local expected="$2"
  [[ -f "$path" ]] || fail "missing file $path"
  local tmp
  tmp="$(mktemp)"
  printf '%s' "$expected" > "$tmp"
  cmp -s "$tmp" "$path" || fail "$path content is incorrect"
  rm -f "$tmp"
}

[[ -f "$ROOT/usr/lib/systemd/system/ledger-ingest.service" ]] || fail "vendor unit is missing"
if ! grep -q -- '--mode stream --listen 0.0.0.0:8080' "$ROOT/usr/lib/systemd/system/ledger-ingest.service"; then
  fail "vendor unit was edited"
fi

mapfile -t dropins < <(find "$DROPIN_DIR" -mindepth 1 -maxdepth 1 -type f -name '*.conf' -printf '%f\n' | sort)
[[ "${#dropins[@]}" -eq 1 ]] || fail "drop-in directory must contain exactly one .conf file"
[[ "${dropins[0]}" == "20-offline-hardening.conf" ]] || fail "drop-in file name is incorrect"

read -r -d '' EXPECT_DROPIN <<'EOF' || true
[Service]
EnvironmentFile=/etc/ledger-ingest/worker.env
ExecStart=
ExecStart=/usr/local/bin/ledger-ingest --config /etc/ledger-ingest/config.yaml --mode ${LEDGER_MODE} --listen ${LEDGER_LISTEN} --spool /var/lib/ledger-ingest/spool --checkpoint /var/lib/ledger-ingest/state/checkpoint.db
User=ledger-ingest
Group=ledger-ingest
SupplementaryGroups=adm
RuntimeDirectory=ledger-ingest
RuntimeDirectoryMode=0750
StateDirectory=ledger-ingest
StateDirectoryMode=0750
LogsDirectory=ledger-ingest
LogsDirectoryMode=0750
UMask=0027
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/ledger-ingest /var/log/ledger-ingest /run/ledger-ingest
Restart=on-failure
RestartSec=5s
EOF
assert_file_exact "$DROPIN" "$EXPECT_DROPIN"$'\n'

read -r -d '' EXPECT_ENV <<'EOF' || true
LEDGER_MODE=batch
LEDGER_LISTEN=127.0.0.1:9191
EOF
assert_file_exact "$ENVFILE" "$EXPECT_ENV"$'\n'
[[ "$(mode_of "$ENVFILE")" == "600" ]] || fail "worker.env mode is not 0600"

read -r -d '' EXPECT_CONFIG <<'EOF' || true
spool: /var/lib/ledger-ingest/spool
checkpoint: /var/lib/ledger-ingest/state/checkpoint.db
log: /var/log/ledger-ingest/current.log
strict_replay: true
EOF
assert_file_exact "$CONFIG" "$EXPECT_CONFIG"$'\n'
[[ "$(mode_of "$CONFIG")" == "640" ]] || fail "config.yaml mode is not 0640"

read -r -d '' EXPECT_SYSUSERS <<'EOF' || true
u ledger-ingest 731 "Ledger Ingest Worker" /var/lib/ledger-ingest /usr/sbin/nologin
m ledger-ingest adm
EOF
assert_file_exact "$SYSUSERS" "$EXPECT_SYSUSERS"$'\n'

read -r -d '' EXPECT_TMPFILES <<'EOF' || true
d /var/lib/ledger-ingest 0750 ledger-ingest ledger-ingest -
d /var/lib/ledger-ingest/spool 0750 ledger-ingest ledger-ingest -
d /var/lib/ledger-ingest/state 0750 ledger-ingest ledger-ingest -
f /var/lib/ledger-ingest/state/checkpoint.db 0640 ledger-ingest ledger-ingest -
d /var/log/ledger-ingest 0750 ledger-ingest adm -
f /var/log/ledger-ingest/current.log 0640 ledger-ingest adm -
EOF
assert_file_exact "$TMPFILES" "$EXPECT_TMPFILES"$'\n'

passwd_entry="$(awk -F: '$1=="ledger-ingest"{print $1":"$3":"$4":"$5":"$6":"$7}' "$ROOT/etc/passwd" 2>/dev/null)"
[[ "$passwd_entry" == "ledger-ingest:731:731:Ledger Ingest Worker:/var/lib/ledger-ingest:/usr/sbin/nologin" ]] || fail "ledger-ingest passwd entry is missing or incorrect"
grep -Eq '^ledger-ingest:x:731:$' "$ROOT/etc/group" || fail "ledger-ingest group entry is missing or incorrect"
grep -Eq '^adm:x:4:ledger-ingest$' "$ROOT/etc/group" || fail "ledger-ingest is not a member of adm"

if ! systemd-analyze verify --root="$ROOT" ledger-ingest.service >/tmp/ledger-ingest-systemd-verify.out 2>&1; then
  cat /tmp/ledger-ingest-systemd-verify.out
  fail "systemd-analyze verify failed"
fi

check_stat() {
  local path="$1" mode="$2" owner_group="$3" type="$4"
  [[ -e "$path" ]] || fail "$path is missing; tmpfiles policy was not applied"
  [[ "$(mode_of "$path")" == "$mode" ]] || fail "$path mode is incorrect"
  [[ "$(owner_group_of "$path")" == "$owner_group" ]] || fail "$path owner/group is incorrect"
  [[ "$(stat -c '%F' "$path")" == "$type" ]] || fail "$path has wrong type"
}

check_stat "$ROOT/var/lib/ledger-ingest" 750 731:731 directory
check_stat "$ROOT/var/lib/ledger-ingest/spool" 750 731:731 directory
check_stat "$ROOT/var/lib/ledger-ingest/state" 750 731:731 directory
check_stat "$ROOT/var/lib/ledger-ingest/state/checkpoint.db" 640 731:731 "regular empty file"
check_stat "$ROOT/var/log/ledger-ingest" 750 731:4 directory
check_stat "$ROOT/var/log/ledger-ingest/current.log" 640 731:4 "regular empty file"

[[ ! -s "$ROOT/var/lib/ledger-ingest/state/checkpoint.db" ]] || fail "checkpoint.db is not empty"
[[ ! -s "$ROOT/var/log/ledger-ingest/current.log" ]] || fail "current.log is not empty"

python3 - <<'PY' || fail "manifest JSON is incorrect"
import json
from pathlib import Path

path = Path("/home/user/unitroot/etc/ledger-ingest/deployment-manifest.json")
data = path.read_bytes()
expected = {
    "service": "ledger-ingest",
    "root": "/home/user/unitroot",
    "dropin": "/etc/systemd/system/ledger-ingest.service.d/20-offline-hardening.conf",
    "sysusers": "/etc/sysusers.d/ledger-ingest.conf",
    "tmpfiles": "/etc/tmpfiles.d/ledger-ingest.conf",
    "environment_file": "/etc/ledger-ingest/worker.env",
    "config": "/etc/ledger-ingest/config.yaml",
    "exec_start": "/usr/local/bin/ledger-ingest --config /etc/ledger-ingest/config.yaml --mode ${LEDGER_MODE} --listen ${LEDGER_LISTEN} --spool /var/lib/ledger-ingest/spool --checkpoint /var/lib/ledger-ingest/state/checkpoint.db",
    "user": "ledger-ingest",
    "directories": [
        "/var/lib/ledger-ingest",
        "/var/lib/ledger-ingest/spool",
        "/var/lib/ledger-ingest/state",
        "/var/log/ledger-ingest",
    ],
    "hardening": [
        "NoNewPrivileges",
        "PrivateTmp",
        "ProtectSystem",
        "ProtectHome",
        "ReadWritePaths",
    ],
}
expected_bytes = json.dumps(expected, separators=(",", ":")).encode() + b"\n"
if data != expected_bytes:
    raise SystemExit(1)
if list(json.loads(data).keys()) != list(expected.keys()):
    raise SystemExit(1)
PY

echo "all checks passed"
echo 1 > /logs/verifier/reward.txt
