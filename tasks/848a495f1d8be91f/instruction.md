# Rebuild a Deterministic OCI Image Layout

The staged root filesystem for `audit-agent` is under `/app/rootfs`, and a broken OCI image layout is under `/app/oci`.

Rebuild `/app/oci` as a complete single-platform OCI image layout for:

- image reference: `audit-agent:2.4.1`
- platform: `linux/amd64`
- created timestamp: `2024-01-01T00:00:00Z`

The final layout must contain only:

- `/app/oci/oci-layout`
- `/app/oci/index.json`
- `/app/oci/blobs/sha256/<manifest digest>`
- `/app/oci/blobs/sha256/<config digest>`
- `/app/oci/blobs/sha256/<compressed layer digest>`

Build the compressed layer from `/app/rootfs` with these rules:

- Include the root filesystem contents except `var/cache/audit-agent/` and `etc/audit-agent/config.yaml.bak`.
- Preserve the executable bit on `usr/local/bin/audit-agent`.
- Preserve the `etc/audit-agent/current.yaml -> config.yaml` symlink.
- Normalize ownership to root/root.
- Normalize all tar entry mtimes and the gzip header mtime to `2024-01-01T00:00:00Z`.
- Use gzip compression for the layer.

Write valid OCI JSON descriptors using OCI media types. All JSON files and JSON blobs should be compact single-line JSON with exactly one trailing newline. The `index.json` descriptor must include the `org.opencontainers.image.ref.name` annotation with value `audit-agent:2.4.1`.
