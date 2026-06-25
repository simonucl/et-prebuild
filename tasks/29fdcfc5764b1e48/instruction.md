# Repair the Deterministic OCI Image Layout

The staged root filesystem for `edgecache` is under `/app/rootfs`. A broken OCI image layout has been started at `/app/oci`.

Repair `/app/oci` so it is a valid single-platform OCI image layout for:

- image reference annotation: `registry.example.test/edgecache:1.2.0`
- operating system: `linux`
- architecture: `amd64`
- creation time: `2024-01-01T00:00:00Z`

The final layout must contain:

- `/app/oci/oci-layout`
- `/app/oci/index.json`
- `/app/oci/blobs/sha256/<manifest-digest>`
- `/app/oci/blobs/sha256/<config-digest>`
- `/app/oci/blobs/sha256/<layer-digest>`

Build the single layer from `/app/rootfs` with deterministic metadata:

- Include the root filesystem contents except `var/cache/edgecache/` and `etc/edgecache/edgecache.toml.tmp`.
- Preserve the executable bit on `usr/local/bin/edgecache`.
- Preserve the `etc/edgecache/current.toml -> edgecache.toml` symlink.
- Normalize regular file modes to `0644` unless executable, directory modes to `0755`, ownership to root/root, and all tar entry timestamps to `2024-01-01T00:00:00Z`.
- Write paths in sorted order and gzip the layer deterministically.

Use OCI media types:

- image index: `application/vnd.oci.image.index.v1+json`
- image manifest: `application/vnd.oci.image.manifest.v1+json`
- image config: `application/vnd.oci.image.config.v1+json`
- layer: `application/vnd.oci.image.layer.v1.tar+gzip`

The JSON files and JSON blobs must be compact single-line JSON with exactly one trailing newline. Descriptor digests and sizes must match the bytes actually written under `blobs/sha256`.
