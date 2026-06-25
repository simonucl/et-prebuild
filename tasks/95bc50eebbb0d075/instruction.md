# Repair the Offline mtree Rootfs Handoff

You are preparing a deterministic offline handoff for the `edge-agent` root filesystem.

The source root filesystem is already staged at:

`/home/user/rootfs_lab/rootfs`

Replace the stale files in:

`/home/user/rootfs_lab/handoff`

Do not use the network. Do not modify, delete, move, or rename anything under `/home/user/rootfs_lab/rootfs`.

Required end state:

1. `/home/user/rootfs_lab/handoff` must contain exactly these three files:
   - `rootfs.tar.gz`
   - `rootfs.mtree`
   - `manifest.json`

2. `rootfs.tar.gz` must be a deterministic gzip-compressed tar archive.
   - The gzip header must have mtime zero and no stored original filename.
   - The tar archive must contain exactly these members, in this order:

```text
rootfs/
rootfs/etc/
rootfs/etc/edge-agent/
rootfs/etc/edge-agent/config.yaml
rootfs/etc/edge-agent/policy.json
rootfs/usr/
rootfs/usr/local/
rootfs/usr/local/bin/
rootfs/usr/local/bin/edge-agent
rootfs/usr/local/bin/edge-agent-current
rootfs/usr/share/
rootfs/usr/share/edge-agent/
rootfs/usr/share/edge-agent/default-policy.json
rootfs/var/
rootfs/var/lib/
rootfs/var/lib/edge-agent/
rootfs/var/lib/edge-agent/state/
rootfs/var/lib/edge-agent/state/initial.db
```

   - Do not include `.git`, `tmp`, cache files, editor backups, or the handoff directory itself.
   - Directory entries must use mode `0755`.
   - Regular files must preserve the source file modes and contents.
   - `rootfs/etc/edge-agent/policy.json` must be a symbolic link with target `../../usr/share/edge-agent/default-policy.json`.
   - `rootfs/usr/local/bin/edge-agent-current` must be stored as a hard link to `rootfs/usr/local/bin/edge-agent`, not as a second regular file.
   - Every tar member must have mtime `2025-01-01 00:00:00 UTC`, numeric uid/gid `0/0`, and owner/group names `root/root`.

3. `rootfs.mtree` must be an mtree-style specification for the packaged tree, with paths relative to `/home/user/rootfs_lab/rootfs`.
   - It must be plain UTF-8 text ending with exactly one trailing newline.
   - It must list the same directory, file, symlink, and hardlink entries as the archive, in the same relative order but without the `rootfs/` prefix.
   - Include SHA-256 digests and byte sizes for regular file contents.
   - Record the symlink target for `etc/edge-agent/policy.json`.
   - Record `nlink=2` for both hard-linked executable paths.

4. `manifest.json` must be minified JSON on one line with exactly one trailing newline. Its top-level keys must appear in this order:

`bundle`, `mtree`, `generated_at`, `archive_sha256`, `mtree_sha256`, `entries`

Required values:

- `bundle`: `rootfs.tar.gz`
- `mtree`: `rootfs.mtree`
- `generated_at`: `2025-01-01T00:00:00Z`
- `archive_sha256`: lowercase SHA-256 hex digest of the final `rootfs.tar.gz`
- `mtree_sha256`: lowercase SHA-256 hex digest of the final `rootfs.mtree`
- `entries`: an array describing the packaged entries in archive order. Each object must use keys in this order: `path`, `type`, `mode`, then type-specific metadata:
  - directories: no additional keys
  - regular files: `size`, `sha256`, and `nlink` when the source file has two links
  - symlinks: `link`
  - hardlinks: `link`, `size`, `sha256`, `nlink`

All work must stay under `/home/user/rootfs_lab`.
