# Repair the Offline Composer Package Repository

An internal Composer repository has been staged at `/app/repo`, but its metadata and dist archive are broken. The package source is available under `/app/pkg-src/package`.

Repair the repository for package `acme/edge-probe` version `2.3.1`.

Create exactly these final repository artifacts:

- `/app/repo/packages.json`
- `/app/repo/dist/acme-edge-probe-2.3.1.zip`

The ZIP archive must contain exactly these file entries, in this order:

1. `composer.json`
2. `LICENSE`
3. `README.md`
4. `bin/edge-probe`
5. `src/Acme/EdgeProbe.php`
6. `src/Acme/Console/ProbeCommand.php`

Use the matching contents from `/app/pkg-src/package`. Do not include development-only files such as tests, editor backups, caches, or directory entries.

Make the archive deterministic:

- all ZIP member timestamps are `1980-01-01 00:00:00`
- ZIP entries are written with Unix metadata
- regular files have mode `0644`, except `bin/edge-probe` which has mode `0755`
- all entries are deflated

Write `/app/repo/packages.json` as compact single-line JSON followed by exactly one newline. It must describe the Composer package with:

- package name `acme/edge-probe`
- version `2.3.1`
- type `library`
- dist type `zip`
- dist URL `dist/acme-edge-probe-2.3.1.zip`
- dist `shasum` equal to the SHA-1 digest of the final ZIP bytes
- PSR-4 autoload prefix `Acme\\EdgeProbe\\` mapped to `src/Acme/`
- binary `bin/edge-probe`
- PHP requirement `>=8.1`

Leave no extra files in `/app/repo` beyond the required metadata file and `dist` directory containing the required ZIP.
