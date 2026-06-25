# Build the offline APT repository handoff

The staging area contains three unsigned Debian packages in `/app/incoming` and an empty repository root at `/app/repo`.

Create a complete offline APT repository under `/app/repo` for suite `acme-stable`, component `main`, and architecture `amd64`.

Required end state:

- Place the packages under the conventional pool paths:
  - `/app/repo/pool/main/e/edge-agent/edge-agent_1.4.0_amd64.deb`
  - `/app/repo/pool/main/e/edge-agent/edge-agent_1.4.1_amd64.deb`
  - `/app/repo/pool/main/r/relayctl/relayctl_0.9.2_amd64.deb`
- Generate `/app/repo/dists/acme-stable/main/binary-amd64/Packages` from the pool using Debian repository tooling, preserving both `edge-agent` versions.
- Generate `/app/repo/dists/acme-stable/main/binary-amd64/Packages.gz` as a deterministic gzip stream.
- Generate `/app/repo/dists/acme-stable/Release` with these metadata fields:
  - `Origin: Acme Offline`
  - `Label: Acme Edge Cache`
  - `Suite: acme-stable`
  - `Codename: acme-stable`
  - `Architectures: amd64`
  - `Components: main`
  - `Description: Acme offline edge relay repository`
  - `Date: Mon, 01 Jul 2024 00:00:00 UTC`
  - `Valid-Until: Mon, 08 Jul 2024 00:00:00 UTC`
- Sign the Release metadata with the local repository signing key provided in `/app/signing/gnupg`, producing both:
  - `/app/repo/dists/acme-stable/InRelease`
  - `/app/repo/dists/acme-stable/Release.gpg`

The signing key is intentionally unprotected and belongs to `Acme Offline Repo <repo@acme.invalid>`. Do not use the network.
