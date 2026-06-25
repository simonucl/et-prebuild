#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

expect_header() {
  local headers="$1"
  local name="$2"
  local value="$3"
  printf '%s\n' "$headers" | tr -d '\r' | grep -Fqx "$name: $value" || fail "missing header $name: $value"
}

conf=/etc/nginx/sites-available/support-console.conf
enabled=/etc/nginx/sites-enabled/support-console.conf
handoff=/home/user/site/handoff
archive="$handoff/support-console-snapshot.tar.gz"
manifest="$handoff/manifest.json"
sums="$handoff/SHA256SUMS"

[ -f "$conf" ] || fail "missing support-console.conf"
[ -L "$enabled" ] || fail "enabled site is not a symlink"
[ "$(readlink "$enabled")" = "$conf" ] || fail "enabled site points to the wrong target"
[ ! -e /etc/nginx/sites-enabled/default ] || fail "default site is still enabled"
nginx -t >/tmp/nginx-test.out 2>&1 || fail "nginx -t failed: $(cat /tmp/nginx-test.out)"

nginx -s stop >/dev/null 2>&1 || true
nginx >/tmp/nginx-start.out 2>&1 || fail "nginx start failed: $(cat /tmp/nginx-start.out)"
trap 'nginx -s stop >/dev/null 2>&1 || true' EXIT
sleep 0.2

curl -fsS http://127.0.0.1:18082/readyz > /tmp/readyz || fail "readyz request failed"
cmp -s /tmp/readyz <(printf 'ok\n') || fail "readyz body is wrong"

curl -fsS -D /tmp/console.headers http://127.0.0.1:18082/console/projects/alpha -o /tmp/console.body || fail "SPA fallback did not return 200"
grep -Fq 'Support Console 2026.06' /tmp/console.body || fail "SPA fallback did not return index.html"
expect_header "$(cat /tmp/console.headers)" "X-Frame-Options" "DENY"
expect_header "$(cat /tmp/console.headers)" "X-Content-Type-Options" "nosniff"

curl -fsS -D /tmp/static.headers http://127.0.0.1:18082/static/app.css -o /tmp/static.body || fail "static asset request failed"
cmp -s /tmp/static.body /srv/releases/current/public/assets/app.css || fail "static asset body is wrong"
expect_header "$(cat /tmp/static.headers)" "Cache-Control" "public, max-age=31536000, immutable"
expect_header "$(cat /tmp/static.headers)" "X-Frame-Options" "DENY"
curl -fsS http://127.0.0.1:18082/static/missing.css -o /tmp/missing.static >/dev/null 2>&1 && fail "missing static asset returned success"

curl -fsS -D /tmp/report.headers http://127.0.0.1:18082/reports/usage.csv -o /tmp/report.body || fail "report request failed"
cmp -s /tmp/report.body /srv/shared/reports/usage.csv || fail "report body is wrong"
expect_header "$(cat /tmp/report.headers)" "Cache-Control" "private, no-store"
expect_header "$(cat /tmp/report.headers)" "X-Frame-Options" "DENY"
curl -fsS http://127.0.0.1:18082/reports/ -o /tmp/report.index >/dev/null 2>&1 && fail "reports directory listing returned success"
curl -fsS http://127.0.0.1:18082/maintenance.html -o /tmp/maintenance >/dev/null 2>&1 && fail "maintenance page is directly reachable"

python3 - <<'PY' || fail "handoff verification failed"
import gzip
import hashlib
import json
import os
import stat
import tarfile
from pathlib import Path

handoff = Path("/home/user/site/handoff")
expected_files = {"support-console-snapshot.tar.gz", "manifest.json", "SHA256SUMS"}
actual_files = {p.name for p in handoff.iterdir() if p.is_file()}
if actual_files != expected_files:
    raise SystemExit(f"handoff contains {sorted(actual_files)}, expected {sorted(expected_files)}")

archive = handoff / "support-console-snapshot.tar.gz"
raw = archive.read_bytes()
if raw[:3] != b"\x1f\x8b\x08":
    raise SystemExit("archive is not gzip")
flags = raw[3]
mtime = int.from_bytes(raw[4:8], "little")
if flags & 0x08 or mtime != 0:
    raise SystemExit("gzip header stores a filename or nonzero mtime")

expected_order = [
    "support-console",
    "support-console/config",
    "support-console/config/enabled.conf",
    "support-console/config/support-console.conf",
    "support-console/public",
    "support-console/public/assets",
    "support-console/public/assets/app.css",
    "support-console/public/assets/app.js",
    "support-console/public/assets/current.css",
    "support-console/public/docs",
    "support-console/public/docs/runbook.html",
    "support-console/public/index.html",
]

members_for_manifest = []
with tarfile.open(archive, "r:gz") as tf:
    members = tf.getmembers()
    names = [m.name for m in members]
    if names != expected_order:
        raise SystemExit(f"unexpected tar member order: {names}")
    by_name = {m.name: m for m in members}
    for m in members:
        if m.mtime != 1800000000:
            raise SystemExit(f"{m.name} has wrong mtime {m.mtime}")
        if m.uid != 0 or m.gid != 0:
            raise SystemExit(f"{m.name} does not use numeric owner/group 0/0")
        if m.isdir():
            typ = "dir"
            if m.mode != 0o755:
                raise SystemExit(f"{m.name} directory mode is {oct(m.mode)}")
            data = b""
            size = 0
        elif m.isfile():
            typ = "file"
            if m.mode != 0o644:
                raise SystemExit(f"{m.name} file mode is {oct(m.mode)}")
            data = tf.extractfile(m).read()
            size = m.size
        elif m.issym():
            typ = "symlink"
            data = b""
            size = 0
        else:
            raise SystemExit(f"{m.name} has unsupported tar type")
        members_for_manifest.append({
            "path": m.name,
            "type": typ,
            "mode": m.mode,
            "bytes": size,
            "sha256": hashlib.sha256(data).hexdigest() if typ == "file" else "",
        })

    if by_name["support-console/config/enabled.conf"].linkname != "support-console.conf":
        raise SystemExit("config/enabled.conf symlink target is wrong")
    if by_name["support-console/public/assets/current.css"].linkname != "app.css":
        raise SystemExit("public/assets/current.css symlink target is wrong")
    conf_bytes = tf.extractfile(by_name["support-console/config/support-console.conf"]).read()

if conf_bytes != Path("/etc/nginx/sites-available/support-console.conf").read_bytes():
    raise SystemExit("archived config does not match active site config")

manifest_path = handoff / "manifest.json"
manifest_raw = manifest_path.read_bytes()
if not manifest_raw.endswith(b"\n") or manifest_raw.endswith(b"\n\n"):
    raise SystemExit("manifest must end with exactly one newline")
if b" " in manifest_raw.rstrip(b"\n") or b"\n" in manifest_raw.rstrip(b"\n"):
    raise SystemExit("manifest is not minified onto one line")
parsed = json.loads(manifest_raw)
expected_manifest = {
    "bundle": "support-console-snapshot.tar.gz",
    "generated_at": "2026-06-25T00:00:00Z",
    "members": members_for_manifest,
    "archive_sha256": hashlib.sha256(raw).hexdigest(),
}
expected_manifest_raw = json.dumps(expected_manifest, separators=(",", ":")).encode() + b"\n"
if manifest_raw != expected_manifest_raw:
    raise SystemExit("manifest content, key order, minification, or hashes are incorrect")

expected_sums = (
    f"{hashlib.sha256(raw).hexdigest()}  support-console-snapshot.tar.gz\n"
    f"{hashlib.sha256(manifest_raw).hexdigest()}  manifest.json\n"
)
if (handoff / "SHA256SUMS").read_text() != expected_sums:
    raise SystemExit("SHA256SUMS is incorrect")
PY

reward=1
echo "$reward" > /logs/verifier/reward.txt
