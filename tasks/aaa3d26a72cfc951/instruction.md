# Repair the Offline VSIX Handoff

You are preparing a deterministic VS Code extension handoff for `acme-log-tools` version `0.9.1`.

The source tree is staged at:

`/home/user/vsix_lab/src/extension`

Replace the stale contents of:

`/home/user/vsix_lab/dist`

Do not use the network.

Required final files in `/home/user/vsix_lab/dist`:

1. `acme-log-tools-0.9.1.vsix`
2. `vsix-manifest.json`
3. `SHA256SUMS`

VSIX package requirements:

- The VSIX is a ZIP archive with no directory entries.
- Every ZIP member must be deflated, have mode `0644`, and have timestamp `2026-06-25 00:00:00`.
- Members must appear in this exact order:
  1. `[Content_Types].xml`
  2. `extension.vsixmanifest`
  3. `extension/package.json`
  4. `extension/README.md`
  5. `extension/LICENSE`
  6. `extension/syntaxes/acme-log.tmLanguage.json`
  7. `extension/snippets/acme-log.json`
- Copy `README.md`, `LICENSE`, `syntaxes/acme-log.tmLanguage.json`, and `snippets/acme-log.json` from the staged source.
- Do not include `NOTES.txt`, stale dist files, editor backups, directory entries, or any other files.

The packaged `extension/package.json` must be minified JSON with exactly these top-level keys in this order:

`name`, `displayName`, `description`, `version`, `publisher`, `license`, `engines`, `categories`, `contributes`

Use these package values:

- `name`: `acme-log-tools`
- `displayName`: `Acme Log Tools`
- `description`: `Offline syntax support for Acme service log captures.`
- `version`: `0.9.1`
- `publisher`: `acme-corp`
- `license`: `MIT`
- `engines.vscode`: `^1.92.0`
- `categories`: `["Programming Languages", "Snippets"]`
- `contributes.languages[0]`:
  - `id`: `acme-log`
  - `aliases`: `["Acme Log", "acme-log"]`
  - `extensions`: `[".acmelog"]`
  - `configuration`: `./syntaxes/acme-log.tmLanguage.json`
- `contributes.snippets[0]`:
  - `language`: `acme-log`
  - `path`: `./snippets/acme-log.json`

The root `[Content_Types].xml` and `extension.vsixmanifest` must describe a normal VSIX package for this extension. Create `vsix-manifest.json` as a minified JSON provenance file describing the VSIX members, their byte sizes, SHA-256 digests, and the VSIX digest. Finish by writing `SHA256SUMS` for `acme-log-tools-0.9.1.vsix` and `vsix-manifest.json`.
