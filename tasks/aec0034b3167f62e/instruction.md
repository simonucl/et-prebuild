# Repair the Offline Terraform Provider Mirror

You are preparing a static Terraform provider network mirror for an air-gapped deployment.
The source files are already staged under `/app/provider-src`, and a broken mirror is staged at:

`/app/mirror/registry.terraform.io/acme/edgecache`

Repair the mirror for provider `registry.terraform.io/acme/edgecache` version `1.2.0` for both platforms:

- `linux_amd64`
- `linux_arm64`

The final mirror directory must contain:

- `index.json`
- `1.2.0.json`
- `terraform-provider-edgecache_1.2.0_linux_amd64.zip`
- `terraform-provider-edgecache_1.2.0_linux_arm64.zip`

Follow Terraform's provider network mirror layout:

- `index.json` lists available versions.
- `1.2.0.json` maps each platform to a relative ZIP URL and a `zh:<sha256-of-zip>` hash.

Build each ZIP from the staged source files. Each archive should contain exactly these root-level entries, in this order:

1. `LICENSE.txt`
2. `README.md`
3. `terraform-provider-edgecache_v1.2.0_x5`

Use the matching platform binary from `/app/provider-src/<platform>/terraform-provider-edgecache_v1.2.0_x5`, and the shared `LICENSE.txt` and `README.md` from `/app/provider-src`.

Make the handoff deterministic: archive member timestamps should be fixed, text files should have regular read permissions, the provider binary should be executable, and the JSON files should be compact single-line JSON with one trailing newline.
