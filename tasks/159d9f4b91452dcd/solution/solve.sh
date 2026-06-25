#!/bin/bash
set -euo pipefail

repo=/home/user/aptrepo
pkgdir="$repo/dists/stable/main/binary-amd64"

mkdir -p "$pkgdir" /home/user/apt-client
cd "$repo"

apt-ftparchive packages pool > "$pkgdir/Packages"
gzip -n -c "$pkgdir/Packages" > "$pkgdir/Packages.gz"

rm -f dists/stable/Release
apt-ftparchive \
  -o APT::FTPArchive::Release::Origin="Acme Offline" \
  -o APT::FTPArchive::Release::Label="Acme Edge" \
  -o APT::FTPArchive::Release::Suite="stable" \
  -o APT::FTPArchive::Release::Codename="stable" \
  -o APT::FTPArchive::Release::Architectures="amd64" \
  -o APT::FTPArchive::Release::Components="main" \
  release dists/stable > dists/stable/Release.new
mv dists/stable/Release.new dists/stable/Release

printf 'deb [trusted=yes] file:/home/user/aptrepo stable main\n' > /home/user/apt-client/sources.list
