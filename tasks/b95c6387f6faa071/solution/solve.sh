#!/bin/bash
set -euo pipefail

cd /home/user/repo_lab

mkdir -p dists/stable/main/binary-amd64

dpkg-scanpackages --arch amd64 pool /dev/null > dists/stable/main/binary-amd64/Packages
gzip -n -9 -c dists/stable/main/binary-amd64/Packages > dists/stable/main/binary-amd64/Packages.gz

packages_path=dists/stable/main/binary-amd64/Packages
packages_gz_path=dists/stable/main/binary-amd64/Packages.gz
packages_sha=$(sha256sum "$packages_path" | awk '{print $1}')
packages_size=$(stat -c '%s' "$packages_path")
packages_gz_sha=$(sha256sum "$packages_gz_path" | awk '{print $1}')
packages_gz_size=$(stat -c '%s' "$packages_gz_path")

cat > dists/stable/Release <<EOF
Archive: stable
Codename: stable
Suite: stable
Component: main
Origin: Acme Offline Ops
Label: Acme Metrics Local Repo
Architectures: amd64
Date: Wed, 15 Jan 2025 00:00:00 +0000
SHA256:
 $packages_sha $packages_size main/binary-amd64/Packages
 $packages_gz_sha $packages_gz_size main/binary-amd64/Packages.gz
EOF

agent_deb=pool/main/a/acme-metrics-agent/acme-metrics-agent_1.4.1_amd64.deb
tools_deb=pool/main/a/acme-metrics-tools/acme-metrics-tools_0.9.0_all.deb
agent_sha=$(sha256sum "$agent_deb" | awk '{print $1}')
tools_sha=$(sha256sum "$tools_deb" | awk '{print $1}')

printf '{"architecture":"amd64","component":"main","packages":[{"name":"acme-metrics-agent","version":"1.4.1","filename":"%s","sha256":"%s"},{"name":"acme-metrics-tools","version":"0.9.0","filename":"%s","sha256":"%s"}],"suite":"stable"}\n' \
  "$agent_deb" "$agent_sha" "$tools_deb" "$tools_sha" > manifest.json
