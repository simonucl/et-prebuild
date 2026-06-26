# Repair the Yarn Classic Offline Mirror

You are preparing a network-free Yarn Classic handoff under `/app/yarn-lab`.

The consumer project is staged at `/app/yarn-lab/app`, and the two package source trees are staged under `/app/yarn-lab/packages`. Replace the stale mirror and lockfile without using the network. Do not modify, delete, move, rename, or retimestamp anything under `/app/yarn-lab/packages`.

Required final state:

1. `/app/yarn-lab/mirror` must contain exactly these two package tarballs:
   - `@acme-edge-flags-1.2.0.tgz`
   - `@acme-policy-table-0.5.1.tgz`

2. Each tarball must be a deterministic gzip-compressed npm package tarball with a single top-level `package/` prefix, no directory entries, gzip mtime `0`, no stored gzip filename, and compression level `9`.

3. `@acme-edge-flags-1.2.0.tgz` must contain exactly these members in this order:
   - `package/package.json`
   - `package/README.md`
   - `package/LICENSE`
   - `package/src/index.js`

   Its generated `package/package.json` must be minified JSON with one trailing newline and keys in this order:
   `name`, `version`, `description`, `type`, `main`, `files`, `license`.

   Values:
   - `name`: `@acme/edge-flags`
   - `version`: `1.2.0`
   - `description`: `Offline edge feature flags`
   - `type`: `module`
   - `main`: `src/index.js`
   - `files`: `["src","README.md","LICENSE"]`
   - `license`: `MIT`

4. `@acme-policy-table-0.5.1.tgz` must contain exactly these members in this order:
   - `package/package.json`
   - `package/index.js`
   - `package/data/defaults.json`

   Its generated `package/package.json` must be minified JSON with one trailing newline and keys in this order:
   `name`, `version`, `description`, `type`, `main`, `files`, `dependencies`, `license`.

   Values:
   - `name`: `@acme/policy-table`
   - `version`: `0.5.1`
   - `description`: `Offline policy defaults table`
   - `type`: `module`
   - `main`: `index.js`
   - `files`: `["index.js","data"]`
   - `dependencies`: `{"@acme/edge-flags":"1.2.0"}`
   - `license`: `Apache-2.0`

5. Every tar member in both package tarballs must use mtime `2026-06-25 00:00:00 UTC`, uid/gid `0/0`, empty uname/gname, and mode `0644`.

6. Write `/app/yarn-lab/yarn.lock` as a Yarn v1 lockfile for the two exact dependencies. It must contain one entry for `@acme/edge-flags@1.2.0` and one entry for `@acme/policy-table@0.5.1`. Each entry must include:
   - `version`
   - `resolved "file:mirror/<tarball>#<sha1>"`
   - `integrity sha512-<base64 sha512 digest>`

   The `@acme/policy-table` entry must also include:

   ```text
   dependencies:
     "@acme/edge-flags" "1.2.0"
   ```

   Use Yarn Classic lockfile formatting with LF line endings and one trailing newline.

7. Write `/app/yarn-lab/.yarnrc` exactly:

   ```text
   yarn-offline-mirror "./mirror"
   yarn-offline-mirror-pruning true
   ```

   End it with one trailing newline.

All final work must stay under `/app/yarn-lab`, and the stale mirror files must be removed.
