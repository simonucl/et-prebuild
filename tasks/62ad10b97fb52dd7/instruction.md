# Deterministic Widget Release Bundle

You are preparing the offline release artifact for the `widget` Python project.
The source tree is already present at:

```text
/home/user/src/widget
```

Create the release directory and exactly three release outputs:

```text
/home/user/release/widget-2.4.1.tar.gz
/home/user/release/SHA256SUMS
/home/user/release/widget-2.4.1.manifest.json
```

The archive must be reproducible. Use `SOURCE_DATE_EPOCH=1704067200`
(`2024-01-01T00:00:00Z`) for tar member modification times. The gzip wrapper
must not store the current time or an original file name.

Archive requirements:

* The archive is gzip-compressed tar.
* It contains only regular files, no directory entries.
* Every member path is prefixed with `widget-2.4.1/`.
* Include exactly these project files and no cache, build, dist, or VCS files:

```text
LICENSE
README.md
docs/usage.md
pyproject.toml
scripts/widget-smoke
src/widget/__init__.py
src/widget/core.py
src/widget/data/defaults.toml
```

* Tar members must appear in the lexical order shown above after adding the
  `widget-2.4.1/` prefix.
* Tar metadata for every member must be normalized: uid `0`, gid `0`, uname
  empty, gname empty, and mtime `1704067200`.
* File modes in the tar must be `0644` for normal files and `0755` for
  `scripts/widget-smoke`.

`SHA256SUMS` must contain exactly one line in the standard `sha256sum` format:

```text
<archive_sha256_two_lowercase_hex_digits_per_byte>  widget-2.4.1.tar.gz
```

`widget-2.4.1.manifest.json` must be minified JSON with a single trailing
newline. Its top-level keys, in order, must be:

```text
name, version, source_date_epoch, archive, sha256, size_bytes, files
```

The `files` value must be an array in the same order as the archive members.
Each file object must have keys in this order:

```text
path, mode, size_bytes, sha256
```

Use paths without the `widget-2.4.1/` prefix inside the manifest's `files`
array. Do not modify the source files.
