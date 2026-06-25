# Repair the Offline Terraform Provider Mirror

You are preparing a static Terraform provider network mirror for the internal provider:

`registry.terraform.io/acme/firewall` version `0.4.2`

The provider source payload is already staged at:

`/home/user/tf-mirror-lab/source/provider`

The broken mirror directory is:

`/home/user/tf-mirror-lab/mirror/registry.terraform.io/acme/firewall`

Do not use the network. Do not modify any file under `/home/user/tf-mirror-lab/source/provider`.

Required end state:

1. Replace the mirror directory so it contains exactly these four files:
   - `index.json`
   - `0.4.2.json`
   - `terraform-provider-acmefirewall_0.4.2_linux_amd64.zip`
   - `SHA256SUMS`

2. Build `terraform-provider-acmefirewall_0.4.2_linux_amd64.zip` as a deterministic ZIP archive.
   - The ZIP must contain exactly these members, in this order:
     - `terraform-provider-acmefirewall_v0.4.2`
     - `LICENSE.txt`
   - Do not include directory entries, `README.md`, temporary files, or any other source files.
   - Use ZIP deflate compression for every member.
   - Normalize every member timestamp to `2024-06-01 00:00:00`.
   - Store Unix permissions as `0755` for the provider executable and `0644` for `LICENSE.txt`.

3. Write Terraform network mirror metadata with LF line endings and exactly one trailing newline.
   - `index.json` must be minified JSON for one available version, with this structure and key order:
     - top-level key `versions`
     - version key `0.4.2`
     - keys `protocols` then `platforms`
     - protocol list `["5.0"]`
     - one platform object with keys `os` then `arch`, values `linux` and `amd64`
   - `0.4.2.json` must be minified JSON with top-level key `archives`.
     - The only archive key is `linux_amd64`.
     - Its object keys must be `url` then `hashes`.
     - `url` is `terraform-provider-acmefirewall_0.4.2_linux_amd64.zip`.
     - `hashes` contains one string: `zh:<lowercase SHA-256 hex digest of the final ZIP>`.

4. `SHA256SUMS` must contain exactly one line:

`<lowercase SHA-256 hex digest of the final ZIP><two spaces>terraform-provider-acmefirewall_0.4.2_linux_amd64.zip`
