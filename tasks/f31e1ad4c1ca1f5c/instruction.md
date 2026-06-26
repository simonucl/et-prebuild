# Repair the Offline CRAN-Style Source Repository

You are preparing an air-gapped CRAN-style source repository for the R package staged at:

`/app/pkg-src/acmeR`

Repair the repository directory:

`/app/repo/src/contrib`

Do not use the network, and do not modify anything under `/app/pkg-src`.

Required final state:

1. `/app/repo/src/contrib` must contain exactly these files:
   - `acmeR_0.2.1.tar.gz`
   - `PACKAGES`
   - `PACKAGES.gz`
   - `PACKAGES.rds`
2. `acmeR_0.2.1.tar.gz` must be a valid R source package built from `/app/pkg-src/acmeR`.
3. The repository metadata must describe only `acmeR` version `0.2.1` and must be generated in the standard R repository format, including the package filename and MD5 checksum.
4. Installing `acmeR` from the local repository with `install.packages(..., repos = "file:///app/repo", type = "source")` must work without network access.

Remove stale repository contents before producing the final handoff.
