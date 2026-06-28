# Debian build-pool retention manifest

You are a Debian release engineer. A build farm has dropped an index of every build
artifact it produced into a **read-only** file:

    /home/user/pool/builds.tsv

It is **tab-separated** with a header line, then one row per build:

    package <TAB> arch <TAB> version <TAB> size_bytes

* `package` — a lower-case identifier.
* `arch` — one of `amd64`, `arm64`, `all`.
* `version` — a **Debian package version string** (it may contain an epoch like
  `1:`, a tilde like `~rc1`, a build/upstream suffix like `+deb12u1`, and a
  Debian revision like `-10`).
* `size_bytes` — a non-negative integer.

The rows are **not** sorted. Do **not** modify `builds.tsv`.

## What "newest" means

Versions MUST be compared using **Debian version ordering** (the algorithm
implemented by `dpkg --compare-versions`), **not** SemVer and **not** plain string
sorting. In particular:

* a tilde sorts *before* anything, even the empty string: `1.0~rc1` < `1.0`;
* an **epoch** dominates the rest: `1:1.0` > `2.0`;
* the Debian **revision** is compared numerically, not lexically: `1.0-2` < `1.0-10`;
* `1.2.11+deb12u1` > `1.2.11`, and `1.2.13~exp` < `1.2.13`;
* a non-numeric upstream segment sorts as Debian rules dictate: `1.0` < `1.0a`.

Within any one `(package, arch)` group all version strings are distinct.

## Your job — produce exactly two files under `/home/user/out/`

Create the directory `/home/user/out/` and write:

### 1. `/home/user/out/manifest.json`

A **single line** of **minified** JSON (no spaces after `:` or `,`), terminated by
exactly one trailing newline (`\n`). The object MUST have this exact shape and key
order:

```
{"source":"/home/user/pool/builds.tsv","groups":[GROUP,...],"totals":{"groups":G,"builds":B,"reclaimable_bytes":R}}
```

Each `GROUP` is, with keys in exactly this order:

```
{"package":<str>,"arch":<str>,"latest":<str>,"count":<int>,"versions":[<str>,...],"superseded":[<str>,...],"reclaimable_bytes":<int>}
```

where, for that `(package, arch)` group:

* `latest` — the highest version by Debian ordering (verbatim string).
* `count` — how many builds are in the group.
* `versions` — **every** version in the group, as exact strings, sorted **ascending**
  by Debian ordering (lowest first, so `latest` is the last element).
* `superseded` — every version **except** `latest`, i.e. `versions` without its last
  element (still ascending).
* `reclaimable_bytes` — the sum of `size_bytes` of the superseded builds.

The `groups` array MUST be ordered by `package` ascending, then `arch` ascending
(ordinary byte/string comparison).

`totals`: `groups` = number of groups; `builds` = total number of rows; and
`reclaimable_bytes` = sum of every group's `reclaimable_bytes`.

### 2. `/home/user/out/reclaim.txt`

One line per group, in the **same order** as the `groups` array, each exactly:

    <package>/<arch>: keep <latest>, supersede <n>, reclaim <bytes> bytes

where `<n>` is the number of superseded builds and `<bytes>` its reclaimable bytes.
Then one final line:

    TOTAL: <total_superseded_builds> builds, <total_reclaimable_bytes> bytes

The file ends with exactly one trailing newline.
