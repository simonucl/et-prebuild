# Deterministic Fleet Agent SquashFS Handoff

Prepare the release handoff under `/app/handoff` from the staged root filesystem at `/app/rootfs`.

Create exactly these files:

- `/app/handoff/fleet-agent-rootfs.sqsh`
- `/app/handoff/manifest.json`
- `/app/handoff/SHA256SUMS`

The SquashFS image must contain the root filesystem contents except for transient files:

- Exclude everything under `var/cache/fleet-agent/`.
- Exclude `etc/fleet-agent/config.yaml.tmp`.
- Preserve regular file executable bits and the `etc/fleet-agent/current.yaml -> config.yaml` symlink.
- Normalize all file ownership in the image to root/root.
- Normalize all inode and filesystem creation timestamps to `2024-01-01T00:00:00Z`.
- Use SquashFS `xz` compression and a 131072-byte block size.

`manifest.json` must be one line of minified JSON followed by exactly one newline. Its keys must appear in this order:

`artifact`, `format`, `compression`, `block_size`, `created_at`, `sha256`, `bytes`

Use these values except where they depend on the final image:

- `artifact`: `fleet-agent-rootfs.sqsh`
- `format`: `squashfs`
- `compression`: `xz`
- `block_size`: `131072`
- `created_at`: `2024-01-01T00:00:00Z`
- `sha256`: lowercase SHA-256 digest of `fleet-agent-rootfs.sqsh`
- `bytes`: decimal byte size of `fleet-agent-rootfs.sqsh`

`SHA256SUMS` must contain exactly one line in the standard two-space format for `fleet-agent-rootfs.sqsh`, followed by exactly one newline.
