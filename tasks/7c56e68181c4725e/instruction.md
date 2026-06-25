# Build an Offline OCI Image Layout

You are preparing a content-addressed OCI image layout for `acme-cache` version `1.2.0`.

The staged input is already present at:

`/home/user/oci-stage`

Create the output directory:

`/home/user/oci-export/acme-cache_1.2.0`

The output must be an OCI image layout containing exactly:

```text
oci-layout
index.json
blobs/sha256/<config digest>
blobs/sha256/<layer digest>
blobs/sha256/<manifest digest>
```

Use the staged root filesystem at `/home/user/oci-stage/rootfs` as the source for a single gzip-compressed tar layer. The layer must include only these paths, emitted in lexical order:

```text
etc
etc/acme-cache
etc/acme-cache/config.yaml
etc/acme-cache/current
usr
usr/local
usr/local/bin
usr/local/bin/acme-cache
var
var/lib
var/lib/acme-cache
var/lib/acme-cache/seed.txt
```

Layer requirements:

- Directories must have mode `0755`.
- Regular files must have mode `0644`, except `usr/local/bin/acme-cache` which must have mode `0755`.
- `etc/acme-cache/current` must be a symbolic link to `config.yaml`.
- All tar entries must use uid/gid `0/0`, empty uname/gname, and mtime `2024-01-01 00:00:00 UTC`.
- The gzip stream must have mtime `0` and must not store an original filename.
- Do not include `tmp`, `tests`, notes, build scratch files, or any source-only files.

Use the metadata in `/home/user/oci-stage/image-meta.json` to build the image config. The config blob must be minified JSON with exactly one trailing newline and these top-level keys in order:

`created`, `architecture`, `os`, `config`, `rootfs`, `history`

Config values:

- `created`: the staged `created` value
- `architecture`: the staged `architecture` value
- `os`: the staged `os` value
- `config`: `{"Env":["PATH=/usr/local/bin:/usr/bin:/bin"],"Cmd":["/usr/local/bin/acme-cache"]}`
- `rootfs`: `{"type":"layers","diff_ids":["sha256:<uncompressed layer sha256>"]}`
- `history`: one object with keys `created` and `created_by`, where `created_by` is `manual offline rootfs import`

The manifest blob must be minified JSON with exactly one trailing newline and these top-level keys in order:

`schemaVersion`, `mediaType`, `config`, `layers`, `annotations`

Use OCI media types:

- manifest: `application/vnd.oci.image.manifest.v1+json`
- config: `application/vnd.oci.image.config.v1+json`
- layer: `application/vnd.oci.image.layer.v1.tar+gzip`

Every descriptor digest and size must match the exact blob bytes in `blobs/sha256/`.

`index.json` must be minified JSON with exactly one trailing newline, with keys `schemaVersion`, `manifests` in that order. It must point to the manifest descriptor and include annotations:

```json
{"org.opencontainers.image.ref.name":"acme-cache:1.2.0"}
```

`oci-layout` must be exactly:

```json
{"imageLayoutVersion":"1.0.0"}
```

with one trailing newline.

Do not modify `/home/user/oci-stage`.
Use only local tools available in the container.
