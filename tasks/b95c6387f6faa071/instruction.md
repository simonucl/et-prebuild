# Repair the Offline APT Repository Handoff

The offline Debian package repository is staged at:

`/home/user/repo_lab`

Repair the repository metadata for the `stable` suite without using the network. The package files in `pool/` are already present and must not be rebuilt, edited, renamed, or moved.

Required end state:

1. Create the binary index files for component `main`, architecture `amd64`:
   - `/home/user/repo_lab/dists/stable/main/binary-amd64/Packages`
   - `/home/user/repo_lab/dists/stable/main/binary-amd64/Packages.gz`

2. Generate the `Packages` index from the repository `pool/` so that it publishes exactly these installable packages:
   - `acme-metrics-agent` version `1.4.1`, architecture `amd64`
   - `acme-metrics-tools` version `0.9.0`, architecture `all`

   The superseded `acme-metrics-agent` version `1.4.0` must remain in `pool/`, but it must not be published in the final index.

3. `Packages.gz` must be a deterministic gzip of `Packages`: no embedded source filename and no embedded timestamp.

4. Create `/home/user/repo_lab/dists/stable/Release` with this exact header and a `SHA256` section for both index files:

   ```text
   Archive: stable
   Codename: stable
   Suite: stable
   Component: main
   Origin: Acme Offline Ops
   Label: Acme Metrics Local Repo
   Architectures: amd64
   Date: Wed, 15 Jan 2025 00:00:00 +0000
   SHA256:
    <sha256> <size> main/binary-amd64/Packages
    <sha256> <size> main/binary-amd64/Packages.gz
   ```

   Use the actual SHA-256 digests and byte sizes of the two files.

5. Create `/home/user/repo_lab/manifest.json` as one minified JSON line with this structure:

   ```json
   {"architecture":"amd64","component":"main","packages":[{"name":"acme-metrics-agent","version":"1.4.1","filename":"pool/main/a/acme-metrics-agent/acme-metrics-agent_1.4.1_amd64.deb","sha256":"<deb_sha256>"},{"name":"acme-metrics-tools","version":"0.9.0","filename":"pool/main/a/acme-metrics-tools/acme-metrics-tools_0.9.0_all.deb","sha256":"<deb_sha256>"}],"suite":"stable"}
   ```

   Replace each `<deb_sha256>` with the actual digest of that `.deb` file. Keep the JSON minified on a single line with one trailing newline.

The final repository must work as an offline `file:` APT source for installing the two published packages. Do not add network sources, signing files, or extra published packages.
