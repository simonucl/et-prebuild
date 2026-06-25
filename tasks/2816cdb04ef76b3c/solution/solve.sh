#!/bin/bash
set -euo pipefail

ROOT=/home/user/unitroot
DROPIN_DIR="$ROOT/etc/systemd/system/ledger-ingest.service.d"

mkdir -p \
  "$DROPIN_DIR" \
  "$ROOT/etc/ledger-ingest" \
  "$ROOT/etc/sysusers.d" \
  "$ROOT/etc/tmpfiles.d"

find "$DROPIN_DIR" -mindepth 1 -maxdepth 1 -type f -name '*.conf' -delete

cat > "$DROPIN_DIR/20-offline-hardening.conf" <<'EOF'
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

cat > "$ROOT/etc/ledger-ingest/worker.env" <<'EOF'
LEDGER_MODE=batch
LEDGER_LISTEN=127.0.0.1:9191
EOF
chmod 0600 "$ROOT/etc/ledger-ingest/worker.env"

cat > "$ROOT/etc/ledger-ingest/config.yaml" <<'EOF'
spool: /var/lib/ledger-ingest/spool
checkpoint: /var/lib/ledger-ingest/state/checkpoint.db
log: /var/log/ledger-ingest/current.log
strict_replay: true
EOF
chmod 0640 "$ROOT/etc/ledger-ingest/config.yaml"

cat > "$ROOT/etc/sysusers.d/ledger-ingest.conf" <<'EOF'
u ledger-ingest 731 "Ledger Ingest Worker" /var/lib/ledger-ingest /usr/sbin/nologin
m ledger-ingest adm
EOF

cat > "$ROOT/etc/tmpfiles.d/ledger-ingest.conf" <<'EOF'
d /var/lib/ledger-ingest 0750 ledger-ingest ledger-ingest -
d /var/lib/ledger-ingest/spool 0750 ledger-ingest ledger-ingest -
d /var/lib/ledger-ingest/state 0750 ledger-ingest ledger-ingest -
f /var/lib/ledger-ingest/state/checkpoint.db 0640 ledger-ingest ledger-ingest -
d /var/log/ledger-ingest 0750 ledger-ingest adm -
f /var/log/ledger-ingest/current.log 0640 ledger-ingest adm -
EOF

systemd-sysusers --root="$ROOT" "$ROOT/etc/sysusers.d/ledger-ingest.conf"
systemd-tmpfiles --create --root="$ROOT" "$ROOT/etc/tmpfiles.d/ledger-ingest.conf"

python3 - <<'PY'
import json
from pathlib import Path

root = Path("/home/user/unitroot")
manifest = {
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
(root / "etc/ledger-ingest/deployment-manifest.json").write_text(
    json.dumps(manifest, separators=(",", ":")) + "\n"
)
PY
