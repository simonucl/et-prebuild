# Repair the Offline Debian Source Repository

You are preparing an air-gapped Debian source repository from the staged source tree:

`/app/source/edge-filter`

Repair the repository rooted at:

`/app/repo`

Do not use the network. Do not modify, delete, move, or rename anything under `/app/source`.

Required final state:

1. The repository must contain exactly these files:
   - `pool/main/e/edge-filter/edge-filter_1.2.0.orig.tar.gz`
   - `pool/main/e/edge-filter/edge-filter_1.2.0-1.debian.tar.xz`
   - `pool/main/e/edge-filter/edge-filter_1.2.0-1.dsc`
   - `dists/stable/main/source/Sources`
   - `dists/stable/main/source/Sources.gz`
   - `dists/stable/Release`
   - `SHA256SUMS`

2. Build a Debian `3.0 (quilt)` source package for source package `edge-filter` version `1.2.0-1`.
   - The orig archive must be a deterministic gzip-compressed tar archive named `edge-filter_1.2.0.orig.tar.gz`.
   - Its tar members must live under top-level directory `edge-filter-1.2.0/` and include exactly `LICENSE`, `README.md`, and `src/filter.py` from the staged source.
   - The debian archive must be a deterministic xz-compressed tar archive named `edge-filter_1.2.0-1.debian.tar.xz`.
   - Its tar members must live under top-level directory `debian/` and include exactly `changelog`, `control`, and `rules` from the staged source.
   - Tar member order must be bytewise sorted by archive path.
   - Normalize tar metadata: regular file modes `0644` except `debian/rules` as `0755`; uid/gid `0`; empty user/group names; mtime `2024-04-02T00:00:00Z`.
   - The gzip wrapper for the orig archive must use mtime `0` and must not store an original filename.
   - The xz stream must be deterministic.

3. Write `edge-filter_1.2.0-1.dsc` as an unsigned Debian source control file with the source package metadata and checksum fields for the two archive files.
   - Include `Checksums-Sha256` and `Files` entries for both archives.
   - Use relative archive filenames in checksum entries, not absolute paths.

4. Write `dists/stable/main/source/Sources` with one source stanza for `edge-filter`.
   - Include the repository `Directory` value `pool/main/e/edge-filter`.
   - Include checksum entries for the `.dsc`, `.orig.tar.gz`, and `.debian.tar.xz` files.
   - Use LF line endings and exactly one trailing newline.

5. Write `Sources.gz` as deterministic gzip data for the exact `Sources` payload, with gzip mtime `0` and no stored original filename.

6. Write `dists/stable/Release` for suite `stable`, component `main`, architecture `source`, and codename `stable`.
   - Include `MD5Sum`, `SHA1`, and `SHA256` sections for `main/source/Sources` and `main/source/Sources.gz`.
   - Use each file's relative path, byte size, and digest.

7. Write `/app/repo/SHA256SUMS` with one line per final repository file, sorted by relative path:

`<sha256 hex><two spaces><relative path>`
