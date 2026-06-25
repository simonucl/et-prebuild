#!/bin/bash
set -u

mkdir -p /logs/verifier

if bash <<'VERIFY'
set -euo pipefail

src=/home/user/evidence/rootfs
out=/home/user/evidence/handoff
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

[ -d "$src" ] || fail "missing source rootfs"
[ -d "$out" ] || fail "missing handoff directory"

actual_files=$(find "$out" -mindepth 1 -maxdepth 1 -type f -printf '%f\n' | LC_ALL=C sort)
expected_files=$'SHA256SUMS\nedge-root.pax.tar.gz\nmanifest.json'
[ "$actual_files" = "$expected_files" ] || fail "handoff directory contains unexpected files: $actual_files"

printf 'policy_version=7\nmode=offline\nallow_debug=false\n' | cmp -s - "$src/etc/edge/policy.conf" || fail "policy.conf was modified"
printf '#!/bin/sh\nset -eu\nprintf "edge ok\\n"\n' | cmp -s - "$src/usr/local/bin/edge-health" || fail "edge-health was modified"
printf 'release=2026.06.25\nchannel=stable\n' | cmp -s - "$src/share/releases/2026.06.25/manifest.txt" || fail "release manifest was modified"
[ "$(readlink "$src/share/current")" = "releases/2026.06.25" ] || fail "source symlink was modified"
[ "$(stat -c '%d:%i' "$src/usr/local/bin/edge-health")" = "$(stat -c '%d:%i' "$src/usr/local/bin/edge-health-current")" ] || fail "source hardlink was modified"
[ "$(getfattr --only-values -n user.release.channel "$src/etc/edge/policy.conf" 2>/dev/null)" = "stable" ] || fail "source xattr was modified"
getfacl -cp "$src/var/lib/edge/cache.db" | grep -qx 'user:backup:r--' || fail "source backup ACL was modified"
[ "$(stat -c '%s' "$src/var/lib/edge/cache.db")" = "1048576" ] || fail "cache.db logical size was modified"

gz_header=$(od -An -tx1 -N10 "$out/edge-root.pax.tar.gz" | tr -d ' \n')
[ "${gz_header:0:6}" = "1f8b08" ] || fail "archive is not gzip"
[ "${gz_header:6:2}" = "00" ] || fail "gzip stream stores filename or extra fields"
[ "${gz_header:8:8}" = "00000000" ] || fail "gzip mtime is not zero"

expected_members=$'edge-root/\nedge-root/etc/\nedge-root/etc/edge/\nedge-root/etc/edge/policy.conf\nedge-root/share/\nedge-root/share/current\nedge-root/share/releases/\nedge-root/share/releases/2026.06.25/\nedge-root/share/releases/2026.06.25/manifest.txt\nedge-root/usr/\nedge-root/usr/local/\nedge-root/usr/local/bin/\nedge-root/usr/local/bin/edge-health\nedge-root/usr/local/bin/edge-health-current\nedge-root/var/\nedge-root/var/lib/\nedge-root/var/lib/edge/\nedge-root/var/lib/edge/cache.db'
actual_members=$(tar -tzf "$out/edge-root.pax.tar.gz")
[ "$actual_members" = "$expected_members" ] || fail "archive members or order are wrong"

python3 - <<'PY'
import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

src = Path("/home/user/evidence/rootfs")
out = Path("/home/user/evidence/handoff")
archive = out / "edge-root.pax.tar.gz"
manifest_path = out / "manifest.json"
expected_tar_names = [
    "edge-root",
    "edge-root/etc",
    "edge-root/etc/edge",
    "edge-root/etc/edge/policy.conf",
    "edge-root/share",
    "edge-root/share/current",
    "edge-root/share/releases",
    "edge-root/share/releases/2026.06.25",
    "edge-root/share/releases/2026.06.25/manifest.txt",
    "edge-root/usr",
    "edge-root/usr/local",
    "edge-root/usr/local/bin",
    "edge-root/usr/local/bin/edge-health",
    "edge-root/usr/local/bin/edge-health-current",
    "edge-root/var",
    "edge-root/var/lib",
    "edge-root/var/lib/edge",
    "edge-root/var/lib/edge/cache.db",
]

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def xattrs(path: Path) -> dict[str, str]:
    output = subprocess.check_output(["getfattr", "--absolute-names", "-d", "-m", "user.*", str(path)], text=True, stderr=subprocess.DEVNULL)
    values = {}
    for line in output.splitlines():
        if line.startswith("user.") and "=" in line:
            key, raw = line.split("=", 1)
            values[key] = raw.strip('"')
    return dict(sorted(values.items()))

def has_backup_acl(path: Path) -> bool:
    acl = subprocess.check_output(["getfacl", "-cp", str(path)], text=True)
    return any(line == "user:backup:r--" for line in acl.splitlines())

with tarfile.open(archive, "r:gz") as tf:
    members = tf.getmembers()
    if [m.name for m in members] != expected_tar_names:
        fail("tar member order is not bytewise sorted under edge-root/")
    for member in members:
        if member.uid != 0 or member.gid != 0:
            fail(f"{member.name} does not use numeric owner/group 0/0")
        if int(member.mtime) != 1782345600:
            fail(f"{member.name} has the wrong normalized mtime")
        if "atime" in member.pax_headers or "ctime" in member.pax_headers:
            fail(f"{member.name} contains atime/ctime pax headers")
    by_name = {m.name: m for m in members}
    if not by_name["edge-root/share/current"].issym() or by_name["edge-root/share/current"].linkname != "releases/2026.06.25":
        fail("share/current is not the required relative symlink")
    if not by_name["edge-root/usr/local/bin/edge-health-current"].islnk() or by_name["edge-root/usr/local/bin/edge-health-current"].linkname != "edge-root/usr/local/bin/edge-health":
        fail("edge-health-current is not archived as a hardlink to edge-health")
    if by_name["edge-root/var/lib/edge/cache.db"].size != 1048576:
        fail("cache.db archive member has wrong logical size")

def expected_manifest() -> bytes:
    paths = [src]
    paths.extend(sorted((p for p in src.rglob("*")), key=lambda p: ("edge-root/" + p.relative_to(src).as_posix()).encode()))
    seen_inodes = {}
    entries = []
    for path in paths:
        rel = "edge-root" if path == src else "edge-root/" + path.relative_to(src).as_posix()
        st = path.lstat()
        entry = {"path": rel, "type": "", "mode": f"{stat.S_IMODE(st.st_mode):04o}"}
        if stat.S_ISDIR(st.st_mode):
            entry["type"] = "dir"
        elif stat.S_ISLNK(st.st_mode):
            entry["type"] = "symlink"
            entry["target"] = os.readlink(path)
        elif stat.S_ISREG(st.st_mode):
            inode = (st.st_dev, st.st_ino)
            if inode in seen_inodes:
                entry["type"] = "hardlink"
                entry["hardlink_to"] = seen_inodes[inode]
            else:
                seen_inodes[inode] = rel
                entry["type"] = "file"
                entry["size"] = st.st_size
                entry["sha256"] = sha256_file(path)
                attrs = xattrs(path)
                if attrs:
                    entry["xattrs"] = attrs
                if has_backup_acl(path):
                    entry["acl"] = "user:backup:r--"
        else:
            fail(f"unsupported source file type: {path}")
        entries.append(entry)
    obj = {
        "archive": "edge-root.pax.tar.gz",
        "format": "posix-pax-gzip",
        "generated_at": "2026-06-25T00:00:00Z",
        "entries": entries,
        "archive_sha256": sha256_file(archive),
    }
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"

raw = manifest_path.read_bytes()
if raw != expected_manifest():
    fail("manifest content, key order, metadata, or trailing newline is incorrect")
try:
    json.loads(raw)
except json.JSONDecodeError as exc:
    fail(f"manifest is not valid JSON: {exc}")

expected_sums = (
    f"{sha256_file(archive)}  edge-root.pax.tar.gz\n"
    f"{sha256_file(manifest_path)}  manifest.json\n"
).encode()
if (out / "SHA256SUMS").read_bytes() != expected_sums:
    fail("SHA256SUMS content is incorrect")

with tempfile.TemporaryDirectory() as td:
    root = Path(td) / "extract"
    root.mkdir()
    subprocess.check_call(["tar", "--acls", "--xattrs", "-xzf", str(archive), "-C", str(root)])
    extracted = root / "edge-root"
    if not extracted.is_dir():
        fail("archive does not extract to edge-root/")
    if os.readlink(extracted / "share/current") != "releases/2026.06.25":
        fail("symlink target was not preserved in archive")
    a = extracted / "usr/local/bin/edge-health"
    b = extracted / "usr/local/bin/edge-health-current"
    if a.stat().st_ino != b.stat().st_ino:
        fail("hard link was not preserved in archive")
    attr = subprocess.check_output(["getfattr", "--only-values", "-n", "user.release.channel", str(extracted / "etc/edge/policy.conf")], text=True, stderr=subprocess.DEVNULL).strip()
    if attr != "stable":
        fail("user.* xattr was not preserved in archive")
    acl = subprocess.check_output(["getfacl", "-cp", str(extracted / "var/lib/edge/cache.db")], text=True)
    if "user:backup:r--" not in acl.splitlines():
        fail("backup ACL was not preserved in archive")
PY
VERIFY
then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
