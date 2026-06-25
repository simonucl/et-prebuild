# Build the netprobe OCI Layout

You are preparing an offline OCI image layout for `netprobe` version `2.1.0`.

The staged input is under:

`/home/user/oci-dual`

Do not use the network. Do not modify anything under `basefs` or `patchfs`.
Replace the stale image layout at:

`/home/user/oci-dual/image`

with a valid single-platform OCI image layout for `linux/amd64`.

Required final state:

1. `image/oci-layout` must contain exactly:

```json
{"imageLayoutVersion":"1.0.0"}
```

followed by one newline.

2. Create two deterministic gzip-compressed layer blobs under
   `image/blobs/sha256/`, in this order:

   - The base layer contains the contents of `basefs`.
   - The update layer contains the contents of `patchfs` plus an OCI whiteout
     file at `etc/netprobe/.wh.defaults.yaml` so that
     `/etc/netprobe/defaults.yaml` is deleted by the update layer.

   For both uncompressed tar streams:

   - entries are sorted by name;
   - all tar entry mtimes are `2025-02-14T12:00:00Z`;
   - all tar owners are numeric `0/0`;
   - PAX `atime` and `ctime` records are absent;
   - the gzip stream has no stored original filename and gzip mtime zero.

3. Create one OCI config JSON blob. It must use:

   - `created`: `2025-02-14T12:00:00Z`
   - `architecture`: `amd64`
   - `os`: `linux`
   - `config.Entrypoint`: `["/usr/local/bin/netprobe"]`
   - `config.Env`: `["NETPROBE_CONFIG=/etc/netprobe/config.yaml"]`
   - `config.WorkingDir`: `/var/lib/netprobe`
   - `config.Labels`: `{"org.opencontainers.image.title":"netprobe","org.opencontainers.image.version":"2.1.0"}`
   - `rootfs.type`: `layers`
   - `rootfs.diff_ids`: the two uncompressed layer digests in base-layer then update-layer order
   - `history`: two entries, both with the same `created` timestamp; their
     `created_by` values must be `import basefs` and `apply offline patch`.

4. Create one OCI manifest JSON blob:

   - `schemaVersion`: `2`
   - `mediaType`: `application/vnd.oci.image.manifest.v1+json`
   - config descriptor media type: `application/vnd.oci.image.config.v1+json`
   - layer descriptor media type: `application/vnd.oci.image.layer.v1.tar+gzip`
   - layer descriptors are ordered base layer, then update layer
   - every descriptor digest and size matches the actual blob bytes.

5. Create `image/index.json` as a minified OCI image index JSON document with
   exactly one manifest descriptor. The descriptor must include:

   - media type `application/vnd.oci.image.manifest.v1+json`
   - platform `{"architecture":"amd64","os":"linux"}`
   - annotations `{"org.opencontainers.image.ref.name":"netprobe:2.1.0-offline"}`

All JSON files and JSON blobs must be minified with exactly one trailing newline.
Leave exactly four files in `image/blobs/sha256`: the base layer, update layer,
config blob, and manifest blob. Blob filenames must be their lowercase SHA-256
hex digest without the `sha256:` prefix.
