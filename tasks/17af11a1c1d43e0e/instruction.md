# Reproducible Rescue Initramfs Handoff

Prepare a deterministic rescue initramfs handoff from the staged filesystem at `/app/rootfs`.

Create exactly these files under `/app/handoff`:

- `/app/handoff/rescue-initramfs.cpio.gz`
- `/app/handoff/manifest.json`
- `/app/handoff/SHA256SUMS`

The initramfs payload must be a gzip-compressed `newc` cpio archive of the root filesystem contents.

Requirements for `rescue-initramfs.cpio.gz`:

- Include the rootfs tree with relative paths rooted at `.`.
- Exclude everything under `var/cache/rescue/`.
- Exclude `etc/rescue/local.key`.
- Preserve directory entries, regular file executable bits, regular file read modes, and the `sbin/init -> ../usr/bin/rescue-init` symlink.
- Normalize all archived uid and gid values to `0`.
- Normalize all archived mtimes to Unix timestamp `1714550400` (`2024-05-01T08:00:00Z`).
- Use deterministic `newc` header fields, including reproducible inode numbering.
- Compress with gzip in a reproducible way: no original filename and gzip header mtime `0`.

`manifest.json` must be one line of minified JSON followed by exactly one newline. Its keys must appear in this order:

`artifact`, `format`, `compression`, `created_at`, `entries`, `sha256`, `bytes`

Use these values except where they depend on the final artifact:

- `artifact`: `rescue-initramfs.cpio.gz`
- `format`: `cpio-newc`
- `compression`: `gzip`
- `created_at`: `2024-05-01T08:00:00Z`
- `entries`: number of entries in the cpio archive, including `.` and the `TRAILER!!!` record
- `sha256`: lowercase SHA-256 digest of `rescue-initramfs.cpio.gz`
- `bytes`: decimal byte size of `rescue-initramfs.cpio.gz`

`SHA256SUMS` must contain exactly one line in the standard two-space format for `rescue-initramfs.cpio.gz`, followed by exactly one newline.
