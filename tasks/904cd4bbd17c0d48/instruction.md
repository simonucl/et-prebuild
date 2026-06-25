# Reproducible Gateway Agent Handoff

You are preparing an offline source-release handoff for `gateway-agent` version `2.7.0`.

The source tree is already present at:

`/home/user/release_src/gateway-agent-2.7.0`

Create the final handoff directory:

`/home/user/handoff`

Do not use the network. Do not modify, delete, or rename anything under `/home/user/release_src`.

Required outputs:

1. `/home/user/handoff/gateway-agent-2.7.0.tar.gz`

   This must be a deterministic gzip-compressed tar archive of the release tree with these requirements:

   - The archive must contain a top-level directory named `gateway-agent-2.7.0/`.
   - Include only the release files and directories. Exclude `.git`, `tmp`, editor backups such as `README.md~`, and `*.tmp` scratch files.
   - Preserve the `docs/current -> runbook.md` symbolic link as a symlink.
   - Store entries in bytewise name order.
   - Store numeric owner and group as `0/0`.
   - Store all directory modes as `0755`.
   - Store regular file modes as `0644`, except `bin/gateway-agent`, which must be `0755`.
   - Store every archive member mtime as `2024-02-03 04:05:06 UTC`.
   - Compress with gzip level 9 and no original filename or timestamp in the gzip header.

2. `/home/user/handoff/manifest.json`

   This must be minified JSON with exactly one trailing newline. The top-level keys must appear in this order:

   - `name`: `gateway-agent`
   - `version`: `2.7.0`
   - `archive`: `gateway-agent-2.7.0.tar.gz`
   - `archive_sha256`: lowercase SHA-256 hex digest of the final archive
   - `contents`: an array sorted by `path`

   Each regular file entry in `contents` must have keys in this order:

   - `path`: path relative to `gateway-agent-2.7.0`
   - `type`: `file`
   - `mode`: four-digit octal mode string
   - `sha256`: lowercase SHA-256 hex digest of that source file's bytes

   The symlink entry must have keys in this order:

   - `path`
   - `type`: `symlink`
   - `target`: the exact symlink target

When finished, `/home/user/handoff` must contain exactly those two output files.
