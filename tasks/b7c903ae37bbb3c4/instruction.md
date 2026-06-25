# Repair the Offline Debian APT Repository

You are preparing an air-gapped Debian-style APT repository for the packages staged at:

`/home/user/apt-lab/packages`

Repair the repository under:

`/home/user/apt-lab/repo`

Do not use the network. Do not modify, delete, move, or rename anything under `/home/user/apt-lab/packages`.

Required final state:

1. The repository must contain exactly these files:
   - `dists/stable/Release`
   - `dists/stable/main/binary-amd64/Packages`
   - `dists/stable/main/binary-amd64/Packages.gz`
   - `pool/main/a/acme-edge-agent/acme-edge-agent_1.4.0_amd64.deb`
   - `pool/main/a/acme-edge-rules/acme-edge-rules_2026.6-1_amd64.deb`
   - `repo-manifest.json`

2. Copy the two `.deb` files from `packages/` into the pool paths above without changing their bytes. Remove stale package files and stale metadata.

3. Build `dists/stable/main/binary-amd64/Packages` with one stanza per package, sorted by package name. Each stanza must use metadata from the package control file and the final pool file bytes. Use exactly these fields and this order:

   `Package`, `Version`, `Architecture`, `Maintainer`, `Installed-Size`, `Depends`, `Section`, `Priority`, `Filename`, `Size`, `MD5sum`, `SHA1`, `SHA256`, `Description`

   `Filename` must be the repository-relative pool path. `Size` is the package file size in bytes. End each stanza with one blank line. Preserve the package description continuation line from the control file.

4. Build `Packages.gz` from the exact `Packages` file using gzip compression level 9, with gzip mtime `0` and no stored original filename.

5. Build `dists/stable/Release` with exactly this field order:

   `Origin`, `Label`, `Suite`, `Codename`, `Date`, `Architectures`, `Components`, `Description`, `MD5Sum`, `SHA1`, `SHA256`

   Use these fixed values:
   - `Origin`: `Acme Edge Offline`
   - `Label`: `Acme Edge Offline`
   - `Suite`: `stable`
   - `Codename`: `stable`
   - `Date`: `Thu, 25 Jun 2026 00:00:00 UTC`
   - `Architectures`: `amd64`
   - `Components`: `main`
   - `Description`: `Offline Acme edge package repository`

   In each checksum section, list `main/binary-amd64/Packages` first and `main/binary-amd64/Packages.gz` second. Each checksum line must contain one leading space, the digest, the decimal size, and the relative path.

6. Create `repo-manifest.json` as minified JSON with exactly one trailing newline and top-level keys in this order:

   `repository`, `suite`, `architecture`, `packages`, `release_sha256`

   `repository` must be `/home/user/apt-lab/repo`, `suite` must be `stable`, and `architecture` must be `amd64`. The `packages` array must list the two packages sorted by package name, each with keys in this order:

   `name`, `version`, `filename`, `sha256`, `size_bytes`

   `release_sha256` must be the lowercase SHA-256 digest of the final `dists/stable/Release` file.
