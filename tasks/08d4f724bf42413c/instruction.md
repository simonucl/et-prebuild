# Repair the Deterministic OCI Image Layout

An incomplete OCI image layout is staged at `/app/oci-layout`, and the source root filesystem is staged at `/app/rootfs`.

Repair `/app/oci-layout` so it contains a single tagged OCI image for:

- reference name: `registry.example.com/acme/edge-gateway:2.4.1`
- architecture: `amd64`
- operating system: `linux`
- created timestamp: `2024-06-02T00:00:00Z`

The finished layout must follow the OCI image layout conventions:

- Top-level `oci-layout` declares image layout version `1.0.0`.
- Top-level `index.json` points to exactly one manifest descriptor tagged with the reference name above.
- Blob files are stored under `/app/oci-layout/blobs/sha256/<digest>`.
- The manifest references one config blob and one gzip-compressed tar layer blob.
- The config JSON includes `architecture`, `os`, `created`, `config.Env`, `config.Entrypoint`, and `rootfs.diff_ids`.
- The layer descriptor digest is the SHA-256 of the compressed layer blob, while `rootfs.diff_ids` contains the SHA-256 of the uncompressed tar layer.

Build the layer from `/app/rootfs`, excluding all contents under `run/` and `tmp/`. The tar stream must be deterministic:

- Include directories and regular files in bytewise sorted path order.
- Store paths without a leading `./`.
- Normalize uid, gid, uname, and gname to root.
- Normalize all tar member mtimes to Unix timestamp `1717286400`.
- Use directory mode `0755`, executable regular-file mode `0755`, and non-executable regular-file mode `0644`.
- Preserve the executable bit of `/usr/local/bin/edge-gateway`.
- Gzip the tar with mtime `0` and no original filename.

All JSON files and JSON blobs must be compact single-line JSON with exactly one trailing newline.

The final `/app/oci-layout` tree must contain only these files:

- `oci-layout`
- `index.json`
- `blobs/sha256/<config digest>`
- `blobs/sha256/<manifest digest>`
- `blobs/sha256/<compressed layer digest>`

