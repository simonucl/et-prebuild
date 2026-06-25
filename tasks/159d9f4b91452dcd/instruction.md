# Repair the Offline APT Repository

You are preparing a file-based APT repository handoff for the internal package `edge-agent` version `1.2.3`.

The repository is already staged at:

`/home/user/aptrepo`

The client-side source list is staged at:

`/home/user/apt-client/sources.list`

Do not use the network, and do not rebuild, replace, move, rename, or modify the `.deb` file under `pool/`.

Required end state:

1. The repository must contain a valid binary package index at `/home/user/aptrepo/dists/stable/main/binary-amd64/Packages`, generated from the repository's `pool/` tree with the package filenames relative to `/home/user/aptrepo`.
2. `/home/user/aptrepo/dists/stable/main/binary-amd64/Packages.gz` must be the deterministic gzip form of that `Packages` file, equivalent to `gzip -n -c Packages`.
3. `/home/user/aptrepo/dists/stable/Release` must describe this repository with:
   - `Origin: Acme Offline`
   - `Label: Acme Edge`
   - `Suite: stable`
   - `Codename: stable`
   - `Architectures: amd64`
   - `Components: main`
   It must also contain correct checksum and size entries for both `main/binary-amd64/Packages` and `main/binary-amd64/Packages.gz`.
4. `/home/user/apt-client/sources.list` must point only at this local repository as a trusted file repository for suite `stable` and component `main`.

When finished, an APT client using only `/home/user/apt-client/sources.list` should be able to update from the local repository and see `edge-agent` version `1.2.3` as the available candidate.
