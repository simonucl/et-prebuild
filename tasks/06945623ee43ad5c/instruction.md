# Edge Root Evidence Handoff

You are preparing an offline evidence bundle for the staged appliance root at:

`/home/user/evidence/rootfs`

Replace the stale contents of:

`/home/user/evidence/handoff`

Do not modify anything under `rootfs`, and do not use the network.

Required end state:

1. Create `/home/user/evidence/handoff/edge-root.pax.tar.gz`.
   - It must be a deterministic gzip stream: gzip mtime zero, maximum compression, and no stored original filename.
   - The uncompressed archive must be a POSIX pax tar archive containing one top-level directory, `edge-root/`, whose contents are exactly the files from `rootfs`.
   - Tar members must be sorted by name.
   - Normalize tar metadata to mtime `2026-06-25T00:00:00Z`, numeric owner/group `0/0`, and no stored atime or ctime pax records.
   - Preserve symbolic links, hard links, sparse-file holes, POSIX ACLs, and `user.*` extended attributes from the source tree.

2. Create `/home/user/evidence/handoff/manifest.json` as minified JSON with exactly one trailing newline. Its top-level keys must appear in this order:

`archive`, `format`, `generated_at`, `entries`, `archive_sha256`

   Use these values:
   - `archive`: `edge-root.pax.tar.gz`
   - `format`: `posix-pax-gzip`
   - `generated_at`: `2026-06-25T00:00:00Z`
   - `archive_sha256`: the SHA-256 digest of the final `edge-root.pax.tar.gz`

   `entries` must list every directory, regular file, hardlink entry, and symlink under `edge-root/` in bytewise sorted path order. Each entry must contain `path`, `type`, and `mode` first. Then add:
   - For normal regular files: `size`, `sha256`, and `xattrs` if any `user.*` xattrs exist.
   - For the second and later names of the same hard-linked file: `hardlink_to`, pointing to the first path for that inode.
   - For symlinks: `target`.
   - For files with a named backup-user ACL entry, include `acl` with the value `user:backup:r--`.

3. Create `/home/user/evidence/handoff/SHA256SUMS` with exactly two lines:

```text
<sha256 of edge-root.pax.tar.gz>  edge-root.pax.tar.gz
<sha256 of manifest.json>  manifest.json
```

The handoff directory must contain exactly those three files.
