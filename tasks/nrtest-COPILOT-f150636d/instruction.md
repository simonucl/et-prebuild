# Debian Pool Curation — `dpkg` Version Ordering

You are the maintainer of an on-premise APT-style package pool. A raw feed of every
build that has ever been published lives (read-only — **do NOT modify, move, or delete
it**) at:

    /home/user/pool/versions.txt

## Input format

Each meaningful line is:

    <name> <version>

* `<name>` is a lower-case package identifier with no spaces.
* `<version>` is a **Debian package version string** as defined by `deb-version(5)`:

      [epoch:]upstream-version[-debian-revision]

  - The optional `epoch` is a non-negative integer; when absent it defaults to `0`.
  - All versions in the feed are syntactically valid.

Blank lines and lines whose first non-space character is `#` are comments and must be
ignored. The same `(name, version)` pair may be listed **more than once**; treat
duplicates as a single occurrence.

## Ordering rules (Debian, NOT SemVer)

Versions MUST be ordered using **Debian version precedence** (`deb-version(5)` /
`dpkg --compare-versions`), which differs from Semantic Versioning. In particular:

* The `epoch` is compared first, numerically (default `0`).
* `upstream-version` and `debian-revision` are each compared by the Debian string
  algorithm: alternating runs of non-digit and digit characters; digit runs compared
  numerically (leading zeros ignored); non-digit runs compared by a modified ASCII order
  in which **a tilde `~` sorts before everything else, even the end of the string**, and
  letters sort before all other non-digit characters.
* Consequently `1.0~rc1` < `1.0`, `1.0a2` < `1.0a10`, and `1:0.1.0` > `9.8.7`.

## What to produce

Create the directory `/home/user/out/` and write exactly two files into it.

### 1. `/home/user/out/manifest.json`

A **single line** of **minified** JSON (no spaces, no indentation) followed by exactly one
trailing newline (`\n`). Keys must appear in **exactly** this order:

```
{"source":"/home/user/pool/versions.txt","packages":[PKG,PKG,...],"total_packages":P,"total_versions":V}
```

Each `PKG` object has its keys in **exactly** this order:

```
{"name":"<name>","versions":[<asc>...],"latest":"<highest>","count":<n>,"superseded":[<asc-without-latest>...]}
```

* `versions` — every **unique** version of the package, sorted **ascending** by Debian
  precedence.
* `latest` — the single highest-precedence version (the last element of `versions`).
* `count` — the number of unique versions (length of `versions`).
* `superseded` — all unique versions **except** `latest`, ascending (i.e. `versions`
  with its last element removed).
* The `packages` array is sorted by `name` in ascending **ASCII** order.
* `total_packages` (`P`) — the number of distinct package names.
* `total_versions` (`V`) — the total number of unique versions summed across all packages.

All JSON strings are plain ASCII; emit them with standard JSON quoting and no escaping
beyond what JSON requires.

### 2. `/home/user/out/latest.txt`

One line per package, sorted by `name` ascending:

    <name> <latest-version>

with a single space separator and a trailing newline after every line (including the
last).

The grader compares both files **byte-for-byte**, so follow the format exactly.
