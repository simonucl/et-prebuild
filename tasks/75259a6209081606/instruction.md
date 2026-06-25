# Deterministic Rescue Initramfs Handoff

Prepare a deterministic initramfs handoff in `/app/handoff` from the staged tree at `/app/initramfs-src`.

Create exactly these files:

- `/app/handoff/rescue-initramfs.cpio.gz`
- `/app/handoff/manifest.json`
- `/app/handoff/SHA256SUMS`

The compressed archive must be a gzip-compressed `newc` cpio archive suitable for a Linux initramfs. Build it from the contents of `/app/initramfs-src` with these constraints:

- Exclude `/app/initramfs-src/etc/rescue/local.secret`.
- Exclude everything under `/app/initramfs-src/var/log/rescue/`.
- Preserve file modes, the `sbin/recovery -> ../usr/bin/recovery` symlink, and the `run/recovery.fifo` FIFO.
- Normalize all archive ownership to root/root.
- Normalize all file, directory, symlink, and FIFO modification times to `2024-02-29T12:34:56Z`.
- Use the `newc` cpio format and gzip compression with no embedded original filename or timestamp.
- Use a deterministic path order.

`manifest.json` must be one line of compact JSON followed by exactly one newline. Its keys must appear in this order:

`artifact`, `format`, `compression`, `created_at`, `sha256`, `bytes`, `entries`

Use these values except where they depend on the final compressed archive:

- `artifact`: `rescue-initramfs.cpio.gz`
- `format`: `cpio-newc`
- `compression`: `gzip-no-name`
- `created_at`: `2024-02-29T12:34:56Z`
- `sha256`: lowercase SHA-256 digest of `rescue-initramfs.cpio.gz`
- `bytes`: decimal byte size of `rescue-initramfs.cpio.gz`
- `entries`: number of archive members, excluding the cpio trailer

`SHA256SUMS` must contain exactly one standard two-space checksum line for `rescue-initramfs.cpio.gz`, followed by exactly one newline.
