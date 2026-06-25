# Repair the Offline TUF Metadata Set

You are preparing a small offline update repository under:

`/home/user/tuf_lab/repository`

The target payloads are already staged under `repository/targets`, and the Ed25519 signing keys are already staged under `/home/user/tuf_lab/keys`. The existing metadata is stale. Replace it without using the network and without modifying target payload files or private keys.

Create exactly these metadata files under `/home/user/tuf_lab/repository/metadata`:

- `root.json`
- `targets.json`
- `snapshot.json`
- `timestamp.json`

Remove stale sidecar files from the metadata directory.

Each metadata file must be a TUF-style JSON envelope with top-level keys in this order:

`signatures`, `signed`

The file must be minified JSON with exactly one trailing newline. The signature must be the lowercase hex Ed25519 signature of the canonical JSON form of the `signed` object. Canonical JSON here means UTF-8 JSON with keys sorted lexicographically and separators `,` and `:` with no extra whitespace.

For each role, use the matching private key:

- `root.json` is signed with `keys/root.ed25519.pem`
- `targets.json` is signed with `keys/targets.ed25519.pem`
- `snapshot.json` is signed with `keys/snapshot.ed25519.pem`
- `timestamp.json` is signed with `keys/timestamp.ed25519.pem`

The `keyid` for a key is the lowercase SHA-256 hex digest of that key's public SubjectPublicKeyInfo DER bytes. The public key value recorded in `root.json` is the standard base64 encoding of those same public DER bytes.

Use these role versions and expiry timestamps:

- root: version `3`, expires `2027-06-25T00:00:00Z`
- targets: version `7`, expires `2026-09-01T00:00:00Z`
- snapshot: version `11`, expires `2026-07-15T00:00:00Z`
- timestamp: version `19`, expires `2026-06-26T00:00:00Z`

`targets.json` must describe exactly these target paths, using the final file bytes:

- `app/config.yaml`
- `bin/edge-tool.sh`

For each target, record `length` in bytes and `hashes.sha256` as lowercase hex.

`snapshot.json` must describe `root.json` and `targets.json`, recording each metadata file's version, byte length, and SHA-256 hash.

`timestamp.json` must describe `snapshot.json`, recording its version, byte length, and SHA-256 hash.

All final work must stay under `/home/user/tuf_lab`.
