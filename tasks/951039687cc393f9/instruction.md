# Git Archive Release Handoff

You are preparing an offline source handoff for `ledger-agent` version `2.1.0`.

The repository is already present at:

`/home/user/archive_lab/repo`

Replace the stale contents of:

`/home/user/archive_lab/out`

with exactly these three files:

1. `/home/user/archive_lab/out/ledger-agent-2.1.0.tar.gz`
2. `/home/user/archive_lab/out/ledger-agent-2.1.0.tar.gz.sha256`
3. `/home/user/archive_lab/out/manifest.json`

Archive requirements:

- The archive must be generated from the Git tag `v2.1.0`.
- Use archive prefix `ledger-agent-2.1.0/`.
- Honor the repository's `.gitattributes`, including ignored export paths and keyword substitution.
- Compress the tar stream with deterministic gzip settings: maximum compression and no stored gzip filename or timestamp.
- Do not modify, delete, retag, or recommit anything in `/home/user/archive_lab/repo`.

Checksum requirements:

- The `.sha256` file must contain exactly one line:

  `<sha256-hex-digest><two spaces>ledger-agent-2.1.0.tar.gz`

- The digest must be computed from the final gzip file.
- End the checksum file with exactly one trailing newline.

Manifest requirements:

Create `/home/user/archive_lab/out/manifest.json` as minified JSON with exactly one trailing newline. The object keys must appear in this order:

`archive`, `tag`, `prefix`, `git_commit`, `gzip`, `sha256`, `entries`

The values must be:

- `archive`: `ledger-agent-2.1.0.tar.gz`
- `tag`: `v2.1.0`
- `prefix`: `ledger-agent-2.1.0/`
- `git_commit`: the full commit hash that `v2.1.0` points to
- `gzip`: `gzip -9 -n`
- `sha256`: the lowercase SHA-256 hex digest of the final gzip file
- `entries`: the tar member list, in archive order, from the uncompressed Git archive stream

All work is local. Do not use the network.
