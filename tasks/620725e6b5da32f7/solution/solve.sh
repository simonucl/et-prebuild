#!/bin/bash
set -euo pipefail

ROOT=/home/user/unitroot

mkdir -p "$ROOT/etc/sysusers.d" "$ROOT/etc/tmpfiles.d" "$ROOT/etc/edge-collector"

cat > "$ROOT/etc/sysusers.d/edge-collector.conf" <<'EOF'
g edge-collector 472 -
u edge-collector 472:edge-collector "Edge Collector" /var/lib/edge-collector /usr/sbin/nologin
m edge-collector adm
EOF

systemd-sysusers --root="$ROOT"

cat > "$ROOT/etc/tmpfiles.d/edge-collector.conf" <<'EOF'
d /var/lib/edge-collector 0750 edge-collector edge-collector -
d /var/lib/edge-collector/spool 0750 edge-collector adm -
d /var/lib/edge-collector/state 0750 edge-collector adm -
C /var/lib/edge-collector/config.json 0640 edge-collector edge-collector - /usr/share/edge-collector/defaults/config.json
f /var/lib/edge-collector/state/checkpoint.json 0640 edge-collector edge-collector -
d /var/log/edge-collector 0750 edge-collector adm -
R /var/cache/edge-collector - - - -
EOF

systemd-tmpfiles --root="$ROOT" --create --remove

cat > "$ROOT/var/lib/edge-collector/state/checkpoint.json" <<'EOF'
{"cursor":"2024-05-14T10:15:00Z","offset":0,"clean_shutdown":true}
EOF
chown 472:472 "$ROOT/var/lib/edge-collector/state/checkpoint.json"
chmod 0640 "$ROOT/var/lib/edge-collector/state/checkpoint.json"

cat > "$ROOT/etc/edge-collector/install-manifest.json" <<'EOF'
{"sysusers":"/etc/sysusers.d/edge-collector.conf","tmpfiles":"/etc/tmpfiles.d/edge-collector.conf","user":"edge-collector","uid":472,"gid":472,"managed_paths":["/var/lib/edge-collector","/var/lib/edge-collector/spool","/var/lib/edge-collector/state","/var/lib/edge-collector/config.json","/var/lib/edge-collector/state/checkpoint.json","/var/log/edge-collector"],"cache_removed":true}
EOF
