# Offline npm Package Handoff

The package source for `@acme/widget-kit` version `1.6.4` is already staged at:

`/home/user/npm-lab/widget-kit`

The handoff directory contains stale files:

`/home/user/npm-lab/handoff`

Replace the stale handoff with exactly these three files:

1. `/home/user/npm-lab/handoff/acme-widget-kit-1.6.4.tgz`
2. `/home/user/npm-lab/handoff/SHA256SUMS`
3. `/home/user/npm-lab/handoff/package-manifest.json`

Do not use the network. Do not modify files under `src/`.

Requirements:

- Build the package tarball using npm's local packaging workflow for the staged package. The package has a lifecycle script that generates the distributable files.
- The tarball name must be npm's normalized scoped-package filename: `acme-widget-kit-1.6.4.tgz`.
- The tarball must contain the package payload that npm would publish for this project, including the generated `dist` files and excluding source-only files, scripts, logs, and stale handoff files.
- `SHA256SUMS` must contain exactly one GNU-style checksum line for the tarball:

```text
<64 lowercase hex chars>  acme-widget-kit-1.6.4.tgz
```

- `package-manifest.json` must be minified JSON with one trailing newline and top-level keys in this exact order:

```json
{"package":"@acme/widget-kit","version":"1.6.4","tarball":"acme-widget-kit-1.6.4.tgz","sha256":"...","sha1":"...","integrity":"...","entry_count":7,"files":[]}
```

Fill the digest fields from the final tarball bytes:

- `sha256`: lowercase SHA-256 hex digest
- `sha1`: lowercase SHA-1 hex digest
- `integrity`: npm-style `sha512-` Subresource Integrity string for the tarball

The `files` array must describe the actual members inside the tarball in archive order. Each entry must use this key order:

```json
{"path":"package/LICENSE","mode":"0644","size":25,"sha256":"..."}
```

Use the file mode stored in the tar header, the byte size stored in the tar header, and the SHA-256 digest of that member's extracted content. End `package-manifest.json` with exactly one newline.
