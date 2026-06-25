#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 1
}

src=/app/module-src
dst=/app/goproxy/example.internal/edge/ratelimit/@v
module=example.internal/edge/ratelimit
version=v0.9.0

cd /

expected_files=$'list\nproxy-manifest.json\nv0.9.0.info\nv0.9.0.mod\nv0.9.0.zip'
actual_files=$(find "$dst" -maxdepth 1 -type f -printf '%f\n' | LC_ALL=C sort)
[[ "$actual_files" == "$expected_files" ]] || fail "proxy directory contains unexpected files: $actual_files"

cmp -s "$src/go.mod" "$dst/$version.mod" || fail "v0.9.0.mod does not match staged go.mod"
[[ "$(cat "$dst/list")" == "$version" ]] || fail "list content is incorrect"
[[ "$(tail -c 1 "$dst/list" | od -An -t x1 | tr -d ' ')" == "0a" ]] || fail "list must end with one newline"
[[ "$(cat "$dst/$version.info")" == '{"Version":"v0.9.0","Time":"2026-06-01T10:30:00Z"}' ]] || fail "v0.9.0.info content is incorrect"
[[ "$(tail -c 1 "$dst/$version.info" | od -An -t x1 | tr -d ' ')" == "0a" ]] || fail "v0.9.0.info must end with one newline"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
(
  cd "$tmp"
  GONOSUMDB='example.internal/*' GOSUMDB=off GOPROXY='file:///app/goproxy' go mod download -json "$module@$version" >download.json
) || fail "go mod download failed through file GOPROXY"

python3 - <<'PY' || fail "archive, manifest, or metadata validation failed"
import hashlib
import json
import stat
import zipfile
from collections import OrderedDict
from pathlib import Path

src = Path("/app/module-src")
dst = Path("/app/goproxy/example.internal/edge/ratelimit/@v")
module = "example.internal/edge/ratelimit"
version = "v0.9.0"
members = ["go.mod", "limiter.go", "limiter_test.go", "README.md"]
expected_names = [f"{module}@{version}/{name}" for name in members]
zip_path = dst / f"{version}.zip"

with zipfile.ZipFile(zip_path) as zf:
    infos = zf.infolist()
    names = [i.filename for i in infos]
    if names != expected_names:
        raise SystemExit(f"unexpected zip members or order: {names}")
    for info, rel in zip(infos, members):
        if info.date_time != (1980, 1, 1, 0, 0, 0):
            raise SystemExit(f"{info.filename} has non-normalized timestamp {info.date_time}")
        mode = (info.external_attr >> 16) & 0o7777
        if mode != 0o644:
            raise SystemExit(f"{info.filename} mode is {oct(mode)}, expected 0o644")
        if info.file_size != (src / rel).stat().st_size:
            raise SystemExit(f"{info.filename} size does not match source")
        if zf.read(info.filename) != (src / rel).read_bytes():
            raise SystemExit(f"{info.filename} content does not match source")

files = []
for rel in members:
    data = (src / rel).read_bytes()
    files.append(OrderedDict([
        ("path", rel),
        ("size_bytes", len(data)),
        ("sha256", hashlib.sha256(data).hexdigest()),
    ]))

expected = OrderedDict([
    ("module", module),
    ("version", version),
    ("files", files),
    ("zip_sha256", hashlib.sha256(zip_path.read_bytes()).hexdigest()),
    ("mod_sha256", hashlib.sha256((dst / f"{version}.mod").read_bytes()).hexdigest()),
    ("info_sha256", hashlib.sha256((dst / f"{version}.info").read_bytes()).hexdigest()),
])
expected_text = json.dumps(expected, separators=(",", ":")) + "\n"
actual_text = (dst / "proxy-manifest.json").read_text()
if actual_text != expected_text:
    raise SystemExit("proxy-manifest.json content, key order, minification, or trailing newline is incorrect")
PY

reward=1
echo "$reward" > /logs/verifier/reward.txt
