#!/bin/bash
set -euo pipefail

repo=/app/repo
suite=acme-stable

mkdir -p \
  "$repo/pool/main/e/edge-agent" \
  "$repo/pool/main/r/relayctl" \
  "$repo/dists/$suite/main/binary-amd64"

cp /app/incoming/edge-agent_1.4.0_amd64.deb "$repo/pool/main/e/edge-agent/"
cp /app/incoming/edge-agent_1.4.1_amd64.deb "$repo/pool/main/e/edge-agent/"
cp /app/incoming/relayctl_0.9.2_amd64.deb "$repo/pool/main/r/relayctl/"

cd "$repo"
dpkg-scanpackages --arch amd64 --multiversion pool > "dists/$suite/main/binary-amd64/Packages"
gzip -9 -n -c "dists/$suite/main/binary-amd64/Packages" > "dists/$suite/main/binary-amd64/Packages.gz"

cat > /tmp/acme-release.conf <<'EOF'
APT::FTPArchive::Release {
  Origin "Acme Offline";
  Label "Acme Edge Cache";
  Suite "acme-stable";
  Codename "acme-stable";
  Architectures "amd64";
  Components "main";
  Description "Acme offline edge relay repository";
  Date "Mon, 01 Jul 2024 00:00:00 UTC";
  Valid-Until "Mon, 08 Jul 2024 00:00:00 UTC";
};
EOF

apt-ftparchive -c /tmp/acme-release.conf release "dists/$suite" > /tmp/acme-Release
mv /tmp/acme-Release "dists/$suite/Release"

GNUPGHOME=/app/signing/gnupg gpg --batch --yes --pinentry-mode loopback \
  --local-user 'repo@acme.invalid' \
  --clearsign --digest-algo SHA256 \
  --output "dists/$suite/InRelease" "dists/$suite/Release"

GNUPGHOME=/app/signing/gnupg gpg --batch --yes --pinentry-mode loopback \
  --local-user 'repo@acme.invalid' \
  --detach-sign --armor --digest-algo SHA256 \
  --output "dists/$suite/Release.gpg" "dists/$suite/Release"

rm -f /tmp/acme-release.conf
