# Offline Git Patch Capsule

You are preparing the offline handoff for `telemetry-agent` version `1.7.3`.

The source repository is already present at:

`/home/user/work/telemetry-agent`

The receiving team only has the base repository at:

`/home/user/work/receiver.git`

Create `/home/user/delivery` and replace any stale contents with exactly these three deliverables:

1. `/home/user/delivery/telemetry-agent-1.7.3.bundle`
2. `/home/user/delivery/telemetry-agent-1.7.3-patches.tar.gz`
3. `/home/user/delivery/manifest.json`

Bundle requirements:

- The bundle must be a real Git bundle created from `/home/user/work/telemetry-agent`.
- It must advertise exactly `refs/heads/release/1.7.3` and `refs/tags/v1.7.3`.
- It must be incremental from tag `v1.7.0`; the commit pointed to by `v1.7.0` must be recorded as a prerequisite, not included as a payload commit.
- It must not advertise `HEAD`, `main`, `experiment/high-cardinality`, or any other refs.
- A clone of `/home/user/work/receiver.git` must be able to verify the bundle, then fetch both the release branch and the `v1.7.3` tag from it.

Patch archive requirements:

- Generate a patch series for every commit in `v1.7.0..refs/heads/release/1.7.3`, oldest first.
- Use standard `git format-patch` mailbox patches.
- The patch archive must be a deterministic gzip-compressed tar archive whose root directory is `patches/`.
- The archive must contain exactly three patch files:
  - `patches/0001-Bump-release-version-to-1.7.3.patch`
  - `patches/0002-Normalize-event-kinds-for-release.patch`
  - `patches/0003-Tighten-telemetry-defaults.patch`
- The patches must apply cleanly with `git am` to a clone of `/home/user/work/receiver.git` and produce the same tree as `refs/heads/release/1.7.3`.
- Normalize the tar metadata: owner and group id `0`, owner and group name `root`, and mtime `2026-02-10 00:00:00 UTC`.
- The gzip layer must not store the original filename and must use timestamp zero.

Manifest requirements:

Create `/home/user/delivery/manifest.json` as minified JSON with exactly one trailing newline. The top-level keys must appear in this order:

`bundle`, `patch_archive`, `source_branch`, `release_tag`, `base_tag`, `prerequisite_commit`, `release_commit`, `included_commits`, `patches`, `bundle_sha256`, `patch_archive_sha256`

The values must be:

- `bundle`: `telemetry-agent-1.7.3.bundle`
- `patch_archive`: `telemetry-agent-1.7.3-patches.tar.gz`
- `source_branch`: `refs/heads/release/1.7.3`
- `release_tag`: `refs/tags/v1.7.3`
- `base_tag`: `v1.7.0`
- `prerequisite_commit`: the full commit id pointed to by `v1.7.0`
- `release_commit`: the full commit id pointed to by `refs/heads/release/1.7.3`
- `included_commits`: an array of objects for the commits in `v1.7.0..refs/heads/release/1.7.3`, oldest first. Each object must have exactly the keys `commit` and `subject`, in that order.
- `patches`: the three patch basenames in order.
- `bundle_sha256`: the lowercase SHA-256 hex digest of the final bundle file.
- `patch_archive_sha256`: the lowercase SHA-256 hex digest of the final patch archive.

Do not modify `/home/user/work/receiver.git`. Do not rewrite history, delete branches, delete tags, or modify tracked files in `/home/user/work/telemetry-agent`.

