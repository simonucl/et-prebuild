#!/bin/bash
set -u

mkdir -p /logs/verifier
ROOT=/home/user/unitroot
fail() {
  echo "FAIL: $1"
  echo 0 > /logs/verifier/reward.txt
  exit 0
}

[ -d "$ROOT" ] || fail "offline root is missing"

[ -f "$ROOT/usr/lib/sysusers.d/edge-collector.conf" ] || fail "packaged sysusers file was removed"
[ -f "$ROOT/usr/lib/tmpfiles.d/edge-collector.conf" ] || fail "packaged tmpfiles file was removed"

expected_sysusers="$(mktemp)"
cat > "$expected_sysusers" <<'EOF'
g edge-collector 472 -
u edge-collector 472:edge-collector "Edge Collector" /var/lib/edge-collector /usr/sbin/nologin
m edge-collector adm
EOF
cmp -s "$expected_sysusers" "$ROOT/etc/sysusers.d/edge-collector.conf" || fail "sysusers override content is wrong"

expected_tmpfiles="$(mktemp)"
cat > "$expected_tmpfiles" <<'EOF'
d /var/lib/edge-collector 0750 edge-collector edge-collector -
d /var/lib/edge-collector/spool 0750 edge-collector adm -
d /var/lib/edge-collector/state 0750 edge-collector adm -
C /var/lib/edge-collector/config.json 0640 edge-collector edge-collector - /usr/share/edge-collector/defaults/config.json
f /var/lib/edge-collector/state/checkpoint.json 0640 edge-collector edge-collector -
d /var/log/edge-collector 0750 edge-collector adm -
R /var/cache/edge-collector - - - -
EOF
cmp -s "$expected_tmpfiles" "$ROOT/etc/tmpfiles.d/edge-collector.conf" || fail "tmpfiles override content is wrong"

grep -qx 'edge-collector:x:472:' "$ROOT/etc/group" || fail "edge-collector group missing or wrong"
grep -Eq '^adm:x:[0-9]+:edge-collector$|^adm:x:[0-9]+:.*,edge-collector(,|$)' "$ROOT/etc/group" || fail "edge-collector is not a member of adm"
grep -qx 'edge-collector:x:472:472:Edge Collector:/var/lib/edge-collector:/usr/sbin/nologin' "$ROOT/etc/passwd" || fail "edge-collector passwd entry missing or wrong"

check_stat() {
  local path="$1" type="$2" mode="$3" uid="$4" gid="$5"
  [ -e "$ROOT$path" ] || fail "$path is missing"
  local actual
  actual="$(stat -c '%F %a %u %g' "$ROOT$path")" || fail "could not stat $path"
  [ "$actual" = "$type $mode $uid $gid" ] || fail "$path stat is '$actual'"
}

check_stat /var/lib/edge-collector directory 750 472 472
check_stat /var/lib/edge-collector/spool directory 750 472 "$(awk -F: '$1=="adm"{print $3}' "$ROOT/etc/group")"
check_stat /var/lib/edge-collector/state directory 750 472 "$(awk -F: '$1=="adm"{print $3}' "$ROOT/etc/group")"
check_stat /var/log/edge-collector directory 750 472 "$(awk -F: '$1=="adm"{print $3}' "$ROOT/etc/group")"
check_stat /var/lib/edge-collector/config.json "regular file" 640 472 472
check_stat /var/lib/edge-collector/state/checkpoint.json "regular file" 640 472 472

cmp -s "$ROOT/usr/share/edge-collector/defaults/config.json" "$ROOT/var/lib/edge-collector/config.json" || fail "config.json was not copied from packaged defaults"
[ ! -e "$ROOT/var/cache/edge-collector" ] || fail "stale cache directory still exists"

python3 - <<'PY' || fail "JSON files are wrong"
import json
from pathlib import Path

root = Path("/home/user/unitroot")

checkpoint_path = root / "var/lib/edge-collector/state/checkpoint.json"
checkpoint_raw = checkpoint_path.read_text()
if checkpoint_raw != '{"cursor":"2024-05-14T10:15:00Z","offset":0,"clean_shutdown":true}\n':
    raise SystemExit("checkpoint is not exact minified JSON")
if json.loads(checkpoint_raw) != {"cursor": "2024-05-14T10:15:00Z", "offset": 0, "clean_shutdown": True}:
    raise SystemExit("checkpoint values are wrong")

manifest_path = root / "etc/edge-collector/install-manifest.json"
manifest_raw = manifest_path.read_text()
expected_raw = '{"sysusers":"/etc/sysusers.d/edge-collector.conf","tmpfiles":"/etc/tmpfiles.d/edge-collector.conf","user":"edge-collector","uid":472,"gid":472,"managed_paths":["/var/lib/edge-collector","/var/lib/edge-collector/spool","/var/lib/edge-collector/state","/var/lib/edge-collector/config.json","/var/lib/edge-collector/state/checkpoint.json","/var/log/edge-collector"],"cache_removed":true}\n'
if manifest_raw != expected_raw:
    raise SystemExit("manifest is not exact minified JSON")
obj = json.loads(manifest_raw)
if list(obj) != ["sysusers", "tmpfiles", "user", "uid", "gid", "managed_paths", "cache_removed"]:
    raise SystemExit("manifest key order is wrong")
PY

echo 1 > /logs/verifier/reward.txt
exit 0
