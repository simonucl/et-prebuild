# Build-artifact retention reconciliation

You are a build engineer. A storage area holds many pre-compiled build artifacts and you
must decide, **per component and per CPU architecture**, which single artifact to *keep*
(the newest version) and which older ones are *superseded*. You then emit a machine-readable
manifest and a human reclaim report. **Do not delete or move any artifact** — only produce
the two report files.

## Input (read-only)

`/home/user/artifacts/incoming` contains only regular files whose names follow this **exact**
pattern:

```
<component>-<version>-<arch>.<ext>
```

* `<component>` — lower-case ASCII letters/digits, contains **no dashes**.
* `<version>` — `MAJOR.MINOR` **or** `MAJOR.MINOR.PATCH`, each part a non-negative integer
  with no leading zeros. A missing `PATCH` is to be treated as `0` **for comparison only**
  (e.g. `2.0` ranks the same as `2.0.0`), but you must reproduce the version string **verbatim**
  in your output (write `2.0`, not `2.0.0`).
* `<arch>` — either `x86_64` or `aarch64`.
* `<ext>` — one of `tar.gz`, `tar.zst`, `whl`.

Versions must be compared **numerically component-by-component**, not as text. (So
`1.10.0` is newer than `1.9.0`, and `0.1.12` is newer than `0.1.2`.) Within any one
`(component, arch)` group the versions are guaranteed distinct after normalization.

## Required outputs

### 1. Output directory

Create `/home/user/artifacts/out` if absent. It must end up with permission mode **exactly 755**.

### 2. Manifest — `/home/user/artifacts/out/manifest.json`

A **minified** JSON document (no spaces, no newlines except a single trailing `\n` that
closes the file). Keys must appear in **exactly** the order shown. Do not hard-code the
example values; derive everything from the input.

```json
{
  "root": "/home/user/artifacts/incoming",
  "components": [
    {
      "name": "<component>",
      "architectures": [
        {
          "arch": "<arch>",
          "keep": {
            "version": "<newest version string, verbatim>",
            "file": "<file name>",
            "sha256": "<hex sha-256 of the file's bytes>",
            "size_bytes": <integer size in bytes>
          },
          "supersede": [
            {
              "version": "<older version string, verbatim>",
              "file": "<file name>",
              "sha256": "<hex sha-256>",
              "size_bytes": <integer>
            }
          ]
        }
      ]
    }
  ],
  "totals": {
    "components": <count of distinct components>,
    "artifacts_total": <count of all input files>,
    "artifacts_superseded": <count of all superseded files>,
    "bytes_superseded": <sum of size_bytes over all superseded files>
  }
}
```

Ordering rules (all ascending):

* `components` — sorted by `name` (ASCII).
* `architectures` — sorted by `arch` (ASCII; so `aarch64` before `x86_64`).
* `keep` — the single newest version in that `(component, arch)` group.
* `supersede` — every **other** version in that group, in **ascending numeric version order**.
* `sha256` — lower-case hex, 64 characters, of the raw file bytes.

### 3. Reclaim report — `/home/user/artifacts/out/reclaim.txt`

Plain text, one line per `(component, arch)` group, in the **same order** the groups appear
in the manifest (component ASCII, then arch ASCII). Each line is **exactly**:

```
<component>/<arch>: keep <kept_version>, supersede <n>, reclaim <bytes> bytes
```

where `<n>` is the number of superseded files in that group and `<bytes>` is the sum of their
`size_bytes`. After all group lines, append exactly one final line:

```
TOTAL: <artifacts_superseded> files, <bytes_superseded> bytes
```

Every line (including the last) is terminated by a single `\n`. No other lines, no header,
no trailing blank line.

## Notes

* Operate entirely as the unprivileged `user`; no root needed.
* Do not modify, rename, or delete anything under `/home/user/artifacts/incoming`.
* An automated grader recomputes the expected manifest and report from the input files and
  compares your output **byte-for-byte**, so the ordering, minification, hashes, and the
  trailing newline all matter.
