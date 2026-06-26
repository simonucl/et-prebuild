# Repair the Offline Terraform Provider Network Mirror

You are preparing a static Terraform provider network mirror for an air-gapped deployment.

The provider binaries are staged under:

`/app/provider-src`

The broken mirror directory to repair is:

`/app/mirror/registry.terraform.io/acme/edge-router`

Do not use the network. Do not modify, delete, or rename anything under `/app/provider-src`.

Repair the mirror for provider `registry.terraform.io/acme/edge-router` version `1.2.3`.

Required final files in `/app/mirror/registry.terraform.io/acme/edge-router`:

1. `index.json`
2. `1.2.3.json`
3. `terraform-provider-edge-router_1.2.3_darwin_arm64.zip`
4. `terraform-provider-edge-router_1.2.3_linux_amd64.zip`
5. `SHA256SUMS`

The mirror metadata must follow Terraform's provider network mirror shape:

- `index.json` must list only version `1.2.3`.
- `1.2.3.json` must contain an `archives` object with entries for `darwin_arm64` and `linux_amd64`.
- Each archive entry must use a relative `url` equal to the corresponding ZIP filename.
- Each archive entry must include a single `zh:<sha256 hex>` hash for the corresponding ZIP archive bytes.

Package requirements:

- Build one ZIP archive per platform from the matching binary in `/app/provider-src/<platform>/`.
- Each ZIP must contain exactly one file named `terraform-provider-edge-router_v1.2.3_x5`.
- Use ZIP deflate compression.
- Normalize the ZIP member timestamp to `2024-03-01 00:00:00`.
- Store Unix mode `0755` on the ZIP member.

Write `SHA256SUMS` with one line per ZIP archive, sorted by filename:

`<sha256 hex><two spaces><zip filename>`

All JSON files must be minified, use LF line endings, and end with exactly one trailing newline.
