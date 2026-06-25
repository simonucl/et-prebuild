#!/bin/bash
set -euo pipefail

mkdir -p /logs/verifier
reward=0
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fail() {
  echo "FAIL: $*" >&2
  echo "$reward" > /logs/verifier/reward.txt
  exit 0
}

repo=/app/repo
suite=acme-stable
pkgdir="$repo/dists/$suite/main/binary-amd64"

required_files=(
  "$repo/pool/main/e/edge-agent/edge-agent_1.4.0_amd64.deb"
  "$repo/pool/main/e/edge-agent/edge-agent_1.4.1_amd64.deb"
  "$repo/pool/main/r/relayctl/relayctl_0.9.2_amd64.deb"
  "$pkgdir/Packages"
  "$pkgdir/Packages.gz"
  "$repo/dists/$suite/Release"
  "$repo/dists/$suite/InRelease"
  "$repo/dists/$suite/Release.gpg"
)

for f in "${required_files[@]}"; do
  [[ -f "$f" ]] || fail "missing required file $f"
done

mapfile -t actual_debs < <(cd "$repo" && find pool -type f -name '*.deb' | LC_ALL=C sort)
expected_debs=(
  "pool/main/e/edge-agent/edge-agent_1.4.0_amd64.deb"
  "pool/main/e/edge-agent/edge-agent_1.4.1_amd64.deb"
  "pool/main/r/relayctl/relayctl_0.9.2_amd64.deb"
)
if [[ "${actual_debs[*]}" != "${expected_debs[*]}" ]]; then
  printf 'actual deb layout:\n%s\n' "${actual_debs[*]}" >&2
  fail "repository pool contains the wrong deb files or paths"
fi

cd "$repo"
dpkg-scanpackages --arch amd64 --multiversion pool > "$tmp/Packages" 2>"$tmp/scan.stderr"
if ! cmp -s "$tmp/Packages" "$pkgdir/Packages"; then
  diff -u "$tmp/Packages" "$pkgdir/Packages" >&2 || true
  fail "Packages does not match dpkg-scanpackages --arch amd64 --multiversion pool"
fi

gzip -9 -n -c "$pkgdir/Packages" > "$tmp/Packages.gz"
if ! cmp -s "$tmp/Packages.gz" "$pkgdir/Packages.gz"; then
  fail "Packages.gz is not deterministic gzip -9 -n output for Packages"
fi

cat > "$tmp/release.conf" <<'EOF'
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
mkdir -p "$tmp/release-root/dists/$suite"
cp -a "$repo/dists/$suite/main" "$tmp/release-root/dists/$suite/"
apt-ftparchive -c "$tmp/release.conf" release "$tmp/release-root/dists/$suite" > "$tmp/Release"
if ! cmp -s "$tmp/Release" "$repo/dists/$suite/Release"; then
  diff -u "$tmp/Release" "$repo/dists/$suite/Release" >&2 || true
  fail "Release does not match apt-ftparchive output with the required metadata"
fi

GNUPGHOME="$tmp/gnupg"
export GNUPGHOME
mkdir -p "$GNUPGHOME"
chmod 700 "$GNUPGHOME"
gpg --batch --quiet --import /app/signing/acme-offline-repo.asc

if ! gpg --batch --verify "$repo/dists/$suite/InRelease" >/tmp/inrelease.verify 2>&1; then
  cat /tmp/inrelease.verify >&2
  fail "InRelease is not a valid clear signature from the repository key"
fi
gpg --batch --decrypt "$repo/dists/$suite/InRelease" > "$tmp/InRelease.payload" 2>/dev/null
if ! cmp -s "$tmp/Release" "$tmp/InRelease.payload"; then
  fail "InRelease signed payload is not the Release file"
fi

if ! gpg --batch --verify "$repo/dists/$suite/Release.gpg" "$repo/dists/$suite/Release" >/tmp/releasegpg.verify 2>&1; then
  cat /tmp/releasegpg.verify >&2
  fail "Release.gpg is not a valid detached signature for Release"
fi

uid="$(gpg --batch --with-colons --list-keys | awk -F: '$1=="uid"{print $10; exit}')"
[[ "$uid" == "Acme Offline Repo <repo@acme.invalid>" ]] || fail "repository key uid is unexpected"

echo 1 > /logs/verifier/reward.txt
