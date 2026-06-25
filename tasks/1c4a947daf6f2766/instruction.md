# Repair the Offline npm Package Handoff

You are preparing an air-gapped npm registry handoff for the scoped package:

`@acme/edge-policy` version `1.3.0`

The source tree is staged at:

`/home/user/npm-lab/src/edge-policy`

Repair the offline registry directory at:

`/home/user/npm-lab/registry/@acme/edge-policy`

Do not use the network and do not modify, delete, move, or rename anything under `/home/user/npm-lab/src`.

Required final state:

1. `/home/user/npm-lab/registry/@acme/edge-policy` must contain exactly:
   - `-/edge-policy-1.3.0.tgz`
   - `index.json`
   - `manifest.json`

2. `-/edge-policy-1.3.0.tgz` must be a deterministic gzip-compressed npm package tarball.
   - The uncompressed tar must contain exactly these regular-file members, in this order, with no directory entries:

```text
package/package.json
package/README.md
package/LICENSE
package/dist/index.js
package/dist/rules.json
package/bin/edge-policy.js
package/types/index.d.ts
```

   - The files other than `package/package.json` must match the corresponding files from the source tree byte-for-byte.
   - The package metadata in `package/package.json` must be minified JSON with exactly one trailing newline and these keys in this order:

```text
name, version, description, type, main, types, bin, files, license, engines
```

   - Use these metadata values:
     - `name`: `@acme/edge-policy`
     - `version`: `1.3.0`
     - `description`: `Offline edge policy compiler`
     - `type`: `module`
     - `main`: `dist/index.js`
     - `types`: `types/index.d.ts`
     - `bin`: `{"edge-policy":"bin/edge-policy.js"}`
     - `files`: `["dist","bin","types","README.md","LICENSE"]`
     - `license`: `MIT`
     - `engines`: `{"node":">=20"}`
   - Every tar member must have mtime `2026-06-25 00:00:00 UTC`, uid/gid `0/0`, empty uname/gname, and mode `0644` except `package/bin/edge-policy.js`, which must be mode `0755`.
   - The gzip wrapper must have mtime `0`, compression level `9`, and no stored original filename.

3. `index.json` must be the offline npm packument for this single version. It must be minified JSON with exactly one trailing newline and top-level keys in this order:

```text
_id, name, dist-tags, versions, time
```

   Required values:
   - `_id`: `@acme/edge-policy`
   - `name`: `@acme/edge-policy`
   - `dist-tags`: `{"latest":"1.3.0"}`
   - `versions` must contain only key `1.3.0`.
   - The `1.3.0` version object must use keys in this order:

```text
name, version, description, license, main, types, bin, dist
```

   - The `dist` object must use keys in this order:

```text
tarball, shasum, integrity, unpackedSize
```

   - `tarball` must be `/@acme/edge-policy/-/edge-policy-1.3.0.tgz`.
   - `shasum` is the lowercase SHA-1 hex digest of the final tarball.
   - `integrity` is `sha512-` followed by the base64 SHA-512 digest of the final tarball.
   - `unpackedSize` is the sum of the byte sizes of the seven tarball member payloads.
   - `time` must be `{"created":"2026-06-25T00:00:00.000Z","modified":"2026-06-25T00:00:00.000Z","1.3.0":"2026-06-25T00:00:00.000Z"}`.

4. `manifest.json` must be minified JSON with exactly one trailing newline and top-level keys in this order:

```text
package, version, tarball, sha1, integrity, size_bytes, files
```

   Values:
   - `package`: `@acme/edge-policy`
   - `version`: `1.3.0`
   - `tarball`: `-/edge-policy-1.3.0.tgz`
   - `sha1`: lowercase SHA-1 hex digest of the final tarball
   - `integrity`: same value used in `index.json`
   - `size_bytes`: byte size of the final tarball
   - `files`: an array listing the seven tar members in tarball order. Each object must have keys `path`, `sha256`, and `size_bytes`, where the digest and size are computed from the member payload bytes.

Remove stale registry files. All final work must stay under `/home/user/npm-lab/registry/@acme/edge-policy`.
