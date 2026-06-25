# Deterministic Recovery Initramfs Handoff

You are preparing an offline recovery initramfs handoff for an edge appliance. The staged filesystem is already present at:

`/home/user/initramfs_lab/rootfs`

Replace the stale files in:

`/home/user/initramfs_lab/out`

Create exactly these deliverables:

1. `/home/user/initramfs_lab/out/recovery-initramfs.cpio.gz`
2. `/home/user/initramfs_lab/out/recovery-initramfs.manifest.json`

The archive must be a gzip-compressed `newc` CPIO stream. Build it from the staged rootfs, but include only this recovery payload, in this exact member order:

```text
.
init
bin
bin/busybox
etc
etc/recovery.conf
lib
lib/modules
lib/modules/6.8.0-edge
lib/modules/6.8.0-edge/modules.dep
sbin
sbin/init
var
var/lib
var/lib/recovery
var/lib/recovery/README
```

Normalize the archive metadata:

- all archived paths are relative and have no leading `./`
- every archived uid and gid is `0`
- every archived mtime is Unix time `0`
- directories are mode `0755`
- `init` and `bin/busybox` are mode `0755`
- regular data files are mode `0644`
- `sbin/init` remains a symbolic link to `../init`
- the gzip wrapper has mtime `0` and does not store an original filename or comment

Do not include temporary files such as `tmp/session.log`.

The manifest must be minified JSON on one line with a trailing newline. Use this key order:

```json
{"format":"newc+gzip","member_count":16,"archive_sha256":"<sha256 of recovery-initramfs.cpio.gz>","uncompressed_sha256":"<sha256 of the decompressed cpio stream>","root":"recovery-root"}
```
