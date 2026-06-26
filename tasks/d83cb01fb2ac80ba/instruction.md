# Repair the Offline Terraform Provider Network Mirror

You are preparing a static Terraform provider network mirror for an air-gapped deployment.

The staged provider payload is under:

`/app/provider-src`

The broken mirror is under:

`/app/mirror/registry.acme.test/acme/edgeaudit`

Do not use the network. Do not modify, move, delete, or rewrite anything under `/app/provider-src`.

Repair the mirror in place for the provider:

- hostname: `registry.acme.test`
- namespace: `acme`
- type: `edgeaudit`
- version: `0.4.2`
- platform: `linux_amd64`
- provider protocol: `5.0`

Required final state:

1. The mirror directory `/app/mirror/registry.acme.test/acme/edgeaudit` must contain exactly these files:
   - `index.json`
   - `0.4.2.json`
   - `terraform-provider-edgeaudit_0.4.2_linux_amd64.zip`
   - `manifest.json`

2. Build `terraform-provider-edgeaudit_0.4.2_linux_amd64.zip` as a deterministic ZIP archive containing exactly these two entries in this order:
   - `terraform-provider-edgeaudit_v0.4.2`
   - `LICENSE.txt`

3. The ZIP entries must use the bytes from `/app/provider-src`, deflate compression, timestamp `2024-01-01 00:00:00`, and Unix modes:
   - `0755` for `terraform-provider-edgeaudit_v0.4.2`
   - `0644` for `LICENSE.txt`

4. `index.json` must be a minified Terraform provider network mirror index for only version `0.4.2`, followed by one trailing newline:

   `{"versions":{"0.4.2":{"protocols":["5.0"]}}}`

5. `0.4.2.json` must be minified JSON followed by one trailing newline. It must describe only the `linux_amd64` archive, with URL `terraform-provider-edgeaudit_0.4.2_linux_amd64.zip` and a single hash entry `zh:<lowercase sha256 hex digest of the final ZIP>`.

6. `manifest.json` must be minified JSON followed by one trailing newline with keys in this order:

   `hostname`, `namespace`, `type`, `version`, `platform`, `archive`, `sha256`, `size`

   The `sha256` and `size` values must describe the final ZIP file.

Remove stale versions, wrong-platform archives, temporary files, backups, and any other files not listed above.
