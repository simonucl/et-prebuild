# Reproducible Rescue Initramfs Handoff

You are preparing a deterministic Linux rescue initramfs handoff.

The staged source filesystem is already present at:

`/home/user/initramfs_lab/source`

Replace the stale files in:

`/home/user/initramfs_lab/out`

Do not modify anything under `source`, and do not use the network.

Required final deliverables:

1. `/home/user/initramfs_lab/out/rescue-initramfs.cpio.gz`
2. `/home/user/initramfs_lab/out/manifest.json`
3. `/home/user/initramfs_lab/out/SHA256SUMS`

Archive requirements:

- The uncompressed archive must be a Linux initramfs `newc` cpio archive.
- It must contain exactly these members in this order, with no leading slash:

```text
.
bin
bin/busybox
bin/sh
etc
etc/issue
etc/mdev.conf
init
sbin
sbin/init
TRAILER!!!
```

- Directory modes must be `0755`.
- Regular file modes must match the source files.
- Symlinks must remain symlinks with these targets:
  - `bin/sh` -> `busybox`
  - `sbin/init` -> `../init`
- Every cpio header must use uid `0`, gid `0`, device numbers `0`, and mtime `2024-05-01T12:00:00Z`.
- The gzip stream must use compression level 9, mtime zero, and no stored original filename.

Manifest requirements:

- Write `/home/user/initramfs_lab/out/manifest.json` as minified JSON with exactly one trailing newline.
- Its top-level keys must appear in this order:

`archive`, `format`, `generated_at`, `members`, `uncompressed_sha256`, `archive_sha256`

- Use:
  - `archive`: `rescue-initramfs.cpio.gz`
  - `format`: `newc-gzip`
  - `generated_at`: `2024-05-01T12:00:00Z`
  - `members`: the ordered list of archive member names excluding `TRAILER!!!`
  - `uncompressed_sha256`: SHA-256 of the uncompressed cpio stream
  - `archive_sha256`: SHA-256 of `rescue-initramfs.cpio.gz`

Checksum requirements:

- `SHA256SUMS` must contain exactly two lines:
  - digest, two spaces, `rescue-initramfs.cpio.gz`
  - digest, two spaces, `manifest.json`
