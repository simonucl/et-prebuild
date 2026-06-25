# Git LFS Capsule Handoff

You are preparing an offline release capsule for the edge telemetry project staged at:

`/home/user/lfs_capsule/source`

The two binary files under `source/assets/` must not be copied directly into the release worktree. Build the handoff under `/home/user/lfs_capsule` with this final layout:

```text
/home/user/lfs_capsule/
  worktree/
    .gitattributes
    README.md
    src/filter.py
    assets/field-model.bin
    assets/sensor-calibration.bin
  objects/sha256/<first-two-hex>/<full-sha256>
  handoff/manifest.json
  handoff/git-lfs-capsule-1.0.0.tar.gz
```

Requirements:

- `worktree/README.md` and `worktree/src/filter.py` must match the source files exactly.
- `worktree/.gitattributes` must contain the Git LFS rule for all `assets/*.bin` files.
- Each `worktree/assets/*.bin` file must be a Git LFS pointer file using the version URL `https://git-lfs.github.com/spec/v1`, the real SHA-256 of the original payload, and the original byte size.
- Each original binary payload must be copied into `objects/sha256/<first-two-hex>/<full-sha256>`.
- `handoff/manifest.json` must describe version `1.0.0`, the archive name, and the two LFS-tracked asset entries.
- `handoff/git-lfs-capsule-1.0.0.tar.gz` must be a reproducible gzip-compressed tar archive containing a top-level `git-lfs-capsule-1.0.0/` directory with `manifest.json`, `worktree/`, and `objects/`.

Do not use the network. Preserve deterministic metadata in the archive: sorted member order, numeric owner/group `0/0`, regular files mode `0644`, directories mode `0755`, and mtime `2024-01-01 00:00:00 UTC`.
