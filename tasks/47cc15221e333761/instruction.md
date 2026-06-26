# Repair the Offline Python Simple Repository

An offline Python package source tree is staged at:

`/app/pkg-src`

A broken static Simple Repository is staged at:

`/app/simple`

Repair the repository for package `acme-edge-sentinel` version `0.6.0`. Do not use the network, and do not modify anything under `/app/pkg-src`.

Required final state:

1. The repository must contain exactly these files under `/app/simple`:
   - `index.html`
   - `acme-edge-sentinel/index.html`
   - `acme-edge-sentinel/acme_edge_sentinel-0.6.0-py3-none-any.whl`
   - `acme-edge-sentinel/acme_edge_sentinel-0.6.0-py3-none-any.whl.metadata`
   - `acme-edge-sentinel/repo-manifest.json`
2. Use the normalized PEP 503 project path `acme-edge-sentinel`, not an underscore variant.
3. Build a deterministic pure-Python wheel from the staged package files. The wheel must:
   - contain the package files from `/app/pkg-src/acme_edge_sentinel`
   - include `METADATA`, `WHEEL`, `entry_points.txt`, and `RECORD` under `acme_edge_sentinel-0.6.0.dist-info/`
   - use the wheel tag `py3-none-any`
   - use deterministic ZIP metadata with timestamp `2024-01-01 00:00:00`
4. Write the `.whl.metadata` file as the exact core metadata used inside the wheel.
5. The project page must link to the wheel with a `#sha256=` URL fragment and a `data-dist-info-metadata="sha256=..."` attribute for the metadata sidecar.
6. Write `repo-manifest.json` as minified JSON describing the normalized package name, version, and SHA256 checksums of the generated repository files.

The finished repository should be usable as a static, air-gapped Python package handoff. Leave no stale files or underscore-named project directories in `/app/simple`.
