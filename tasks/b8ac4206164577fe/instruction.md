# Repair the Offline Ansible Collection Handoff

You are preparing an offline Ansible Galaxy-style collection handoff for:

- namespace: `acme`
- collection name: `edge_ops`
- version: `1.2.3`

The source collection is staged at:

`/app/collection-src/acme/edge_ops`

The broken handoff directory is:

`/app/galaxy`

Do not use the network. Do not modify, delete, move, rename, or retimestamp anything under `/app/collection-src`.

Replace the stale handoff with exactly these files:

- `/app/galaxy/artifacts/acme-edge_ops-1.2.3.tar.gz`
- `/app/galaxy/index.json`
- `/app/galaxy/SHA256SUMS`

The collection artifact must be a deterministic gzip-compressed tar archive. The gzip stream must use compression level 9, mtime `0`, and no stored original filename. The tar archive must contain no directory entries and exactly these regular-file members, in this order:

1. `MANIFEST.json`
2. `FILES.json`
3. `README.md`
4. `LICENSE`
5. `docs/usage.md`
6. `plugins/module_utils/client.py`
7. `plugins/modules/edge_status.py`
8. `roles/edge_agent/tasks/main.yml`

Normalize every tar member to mode `0644`, uid/gid `0/0`, empty owner/group names, and mtime `2024-06-01T00:00:00Z`.

The six payload files must match the source bytes exactly. Do not package `galaxy.yml`, tests, temporary files, editor backups, stale handoff files, or directory entries.

Write `FILES.json` as compact single-line JSON followed by exactly one newline. Its top-level keys must appear in this order: `files`, `format`. The `files` array must list the six payload files in archive order. Each file entry must use key order `name`, `ftype`, `chksum_type`, `chksum_sha256`, `size`, with:

- `ftype`: `file`
- `chksum_type`: `sha256`
- `chksum_sha256`: lowercase SHA-256 hex digest of the source file bytes
- `size`: decimal byte size of the source file

Write `MANIFEST.json` as compact single-line JSON followed by exactly one newline. Its top-level keys must appear in this order: `collection_info`, `file_manifest_file`, `format`. Use this collection metadata:

- `collection_info.namespace`: `acme`
- `collection_info.name`: `edge_ops`
- `collection_info.version`: `1.2.3`
- `collection_info.authors`: `["Acme Platform <platform@acme.invalid>"]`
- `collection_info.readme`: `README.md`
- `collection_info.tags`: `["edge","offline","automation"]`
- `collection_info.description`: `Offline automation helpers for Acme edge gateways.`
- `collection_info.license`: `[]`
- `collection_info.license_file`: `LICENSE`
- `collection_info.dependencies`: `{}`
- `collection_info.repository`: `https://git.example.invalid/acme/edge-ops`
- `collection_info.documentation`: `https://docs.example.invalid/acme/edge-ops`
- `collection_info.homepage`: `https://example.invalid/acme/edge-ops`
- `collection_info.issues`: `https://git.example.invalid/acme/edge-ops/issues`

The `file_manifest_file` object must use key order `name`, `ftype`, `chksum_type`, `chksum_sha256`, `format` and must describe the final `FILES.json` bytes. Set both top-level `format` values to `1`.

Write `/app/galaxy/index.json` as compact single-line JSON followed by exactly one newline. Its top-level keys must appear in this order:

`format`, `namespace`, `name`, `version`, `artifact`, `sha256`, `size_bytes`, `manifest_sha256`, `files_sha256`

The digest and size fields must describe the final artifact, `MANIFEST.json`, and `FILES.json`.

Write `/app/galaxy/SHA256SUMS` with exactly one line:

`<sha256 of artifacts/acme-edge_ops-1.2.3.tar.gz>  artifacts/acme-edge_ops-1.2.3.tar.gz`

Leave no stale versions, temporary directories, loose metadata, or extra files under `/app/galaxy`.
