#!/bin/bash
set -euo pipefail

mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
cat > /etc/nginx/sites-available/support-console.conf <<'EOF'
server {
    listen 18082 default_server;
    server_name _;

    include /etc/nginx/snippets/support_security_headers.conf;

    location /console/ {
        alias /srv/releases/current/public/;
        try_files $uri $uri/ /console/index.html;
    }

    location /static/ {
        alias /srv/releases/current/public/assets/;
        try_files $uri =404;
        include /etc/nginx/snippets/support_security_headers.conf;
        add_header Cache-Control "public, max-age=31536000, immutable" always;
    }

    location /reports/ {
        alias /srv/shared/reports/;
        autoindex off;
        try_files $uri =404;
        include /etc/nginx/snippets/support_security_headers.conf;
        add_header Cache-Control "private, no-store" always;
    }

    location = /readyz {
        default_type text/plain;
        return 200 "ok\n";
    }

    location = /maintenance.html {
        internal;
        alias /srv/shared/errors/maintenance.html;
    }

    error_page 503 /maintenance.html;
}
EOF

rm -f /etc/nginx/sites-enabled/default
ln -sfn /etc/nginx/sites-available/support-console.conf /etc/nginx/sites-enabled/support-console.conf
nginx -t

handoff=/home/user/site/handoff
rm -rf "$handoff"
mkdir -p "$handoff"

stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/support-console/config" "$stage/support-console/public"
cp /etc/nginx/sites-available/support-console.conf "$stage/support-console/config/support-console.conf"
ln -s support-console.conf "$stage/support-console/config/enabled.conf"
cp -a /srv/releases/current/public/. "$stage/support-console/public/"
find "$stage/support-console" -type d -exec chmod 0755 {} +
find "$stage/support-console" -type f -exec chmod 0644 {} +

tar --sort=name \
  --mtime='@1800000000' \
  --owner=0 --group=0 --numeric-owner \
  --format=ustar \
  -cf - -C "$stage" support-console | gzip -n > "$handoff/support-console-snapshot.tar.gz"

python3 - <<'PY'
import gzip
import hashlib
import json
import tarfile
from pathlib import Path

handoff = Path("/home/user/site/handoff")
archive = handoff / "support-console-snapshot.tar.gz"
members = []
with tarfile.open(archive, "r:gz") as tf:
    for member in tf.getmembers():
        if member.isdir():
            typ = "dir"
            data = b""
        elif member.issym():
            typ = "symlink"
            data = b""
        elif member.isfile():
            typ = "file"
            data = tf.extractfile(member).read()
        else:
            raise SystemExit(f"unsupported tar member: {member.name}")
        members.append({
            "path": member.name,
            "type": typ,
            "mode": member.mode,
            "bytes": member.size if typ == "file" else 0,
            "sha256": hashlib.sha256(data).hexdigest() if typ == "file" else "",
        })

manifest = {
    "bundle": "support-console-snapshot.tar.gz",
    "generated_at": "2026-06-25T00:00:00Z",
    "members": members,
    "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
}
(handoff / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
sha_archive = hashlib.sha256(archive.read_bytes()).hexdigest()
sha_manifest = hashlib.sha256((handoff / "manifest.json").read_bytes()).hexdigest()
(handoff / "SHA256SUMS").write_text(
    f"{sha_archive}  support-console-snapshot.tar.gz\n"
    f"{sha_manifest}  manifest.json\n"
)
PY
