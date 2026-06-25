# Repair the Offline Debian APT Repository

You are preparing a small air-gapped Debian-style APT repository for the packages staged in:

`/home/user/apt_lab/packages`

Repair the repository under:

`/home/user/apt_lab/repo`

Do not use the network, and do not modify, delete, or rewrite anything under `/home/user/apt_lab/packages`.

Required final state:

1. Copy the two staged `.deb` files into the repository pool without changing their bytes:
   - `pool/main/e/edge-meter/edge-meter_1.4.0-1_amd64.deb`
   - `pool/main/e/edge-relay/edge-relay_0.8.2-2_amd64.deb`

2. Rebuild the binary package index at:
   - `dists/bookworm/main/binary-amd64/Packages`
   - `dists/bookworm/main/binary-amd64/Packages.gz`

   The `Packages` file must contain one record per package, sorted by package name. Use the control metadata from the `.deb` files and write fields in this exact order when present:

   `Package`, `Version`, `Architecture`, `Maintainer`, `Installed-Size`, `Depends`, `Section`, `Priority`, `Homepage`, `Filename`, `Size`, `SHA256`, `Description`

   `Filename` must be relative to the repository root. `Size` is the decimal byte size of the copied `.deb`. `SHA256` is the lowercase SHA-256 digest of the copied `.deb`. Put one blank line after each package record.

   `Packages.gz` must be a deterministic gzip stream of the `Packages` bytes: compression level 9, gzip mtime 0, and no stored original filename.

3. Rebuild `dists/bookworm/Release` with exactly these header fields and values:

   ```text
   Origin: Acme Offline
   Label: Acme Edge Apt
   Suite: stable
   Codename: bookworm
   Date: Thu, 25 Jun 2026 00:00:00 UTC
   Architectures: amd64
   Components: main
   Description: Acme edge offline repository
   ```

   Then include a `SHA256:` section with checksums for these two files, in this order:

   ```text
    <sha256> <size> main/binary-amd64/Packages
    <sha256> <size> main/binary-amd64/Packages.gz
   ```

   End the file with exactly one trailing newline.

4. Write `/home/user/apt_lab/repo/manifest.json` as minified JSON with exactly one trailing newline and top-level keys in this order:

   `repo`, `codename`, `suite`, `architecture`, `packages`, `release_sha256`, `packages_sha256`, `packages_gz_sha256`

   Use `/home/user/apt_lab/repo`, `bookworm`, `stable`, and `amd64` for the first four values. The `packages` array must be:

   ```json
   ["edge-meter=1.4.0-1","edge-relay=0.8.2-2"]
   ```

5. Remove stale repository files. The final repository must contain exactly the required pool package files, `Packages`, `Packages.gz`, `Release`, and `manifest.json`.
