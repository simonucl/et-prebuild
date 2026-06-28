# Reproducible Source Release Package

You are preparing the offline source release for `acme-widget` version `1.4.2`.
The source tree already exists at:

`/home/user/release/src/acme-widget-1.4.2`

Create the output directory `/home/user/release/out` and place exactly these two release artifacts in it:

1. `/home/user/release/out/acme-widget-1.4.2-src.tar.gz`
2. `/home/user/release/out/acme-widget-1.4.2-src.tar.gz.sha256`

Archive requirements:

- The archive root must be the single directory `acme-widget-1.4.2/`.
- Include normal project files, directories, executable bits, and symbolic links from the source tree.
- Exclude all VCS/cache/build/release scratch content:
  - any `.git` directory and its contents
  - any `.pytest_cache` directory and its contents
  - any `build` directory and its contents
  - any `dist` directory and its contents
  - any file whose name ends in `.tmp`
  - any file whose name ends in `~`
- The tar entries must be sorted by name.
- Every archive entry must have owner id `0`, group id `0`, owner name `root`, group name `root`.
- Every archive entry must have modification time exactly `2024-01-01 00:00:00 UTC`.
- The gzip layer must not store the original file name or timestamp.

Checksum requirements:

- The `.sha256` file must contain exactly one line:

  `<sha256-hex-digest><two spaces>acme-widget-1.4.2-src.tar.gz`

- The digest must be computed from the final gzip file you created.
- End the checksum file with a single trailing newline.

Do not modify, move, rename, or delete anything under `/home/user/release/src`.
