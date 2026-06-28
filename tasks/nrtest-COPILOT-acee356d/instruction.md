# Package Registry Upgrade-Plan Generator

You are a release engineer for an on-premise package registry. You must produce an
**upgrade plan** that tells operations which artefacts are superseded and how many bytes
can be safely reclaimed, while always keeping the newest *stable, non-yanked* release of
every package.

## Input (read-only)

The directory `/home/user/registry` contains one metadata file per published artefact.
Each file is named:

```
<package>@<version>.meta
```

* `<package>` is a lower-case ASCII identifier (no `@`).
* `<version>` is a [Semantic Versioning 2.0.0](https://semver.org/) string of the form
  `MAJOR.MINOR.PATCH` optionally followed by a pre-release suffix, e.g. `2.0.0-rc.10`,
  `3.0.0-alpha.1`.

Each file contains exactly these three lines:

```
size_bytes=<integer>
published=<unix-epoch-seconds>
yanked=<true|false>
```

Do **not** modify, move, or delete anything under `/home/user/registry`.

## Definitions (follow precisely)

For every package, consider all of its versions:

* **`latest_stable`** — the highest-precedence version that is **NOT yanked** and is a
  **stable** release (i.e. has *no* pre-release suffix). Version precedence MUST follow
  the SemVer 2.0.0 rules:
  * compare `MAJOR`, then `MINOR`, then `PATCH` **numerically** (so `1.10.0` > `1.9.0`);
  * a version *with* a pre-release suffix has **lower** precedence than the otherwise
    equal stable version;
  * pre-release suffixes are compared identifier-by-identifier (split on `.`): purely
    numeric identifiers are compared numerically, others lexically (ASCII); a numeric
    identifier is always lower than a non-numeric one; if all preceding identifiers are
    equal the version with *more* identifiers is higher (`1.0.0-alpha` < `1.0.0-alpha.1`).
  Every package in this registry is guaranteed to have at least one such version.

* **`superseded`** — every version of the package **except** `latest_stable`. Each
  superseded entry is assigned exactly one `reason`, chosen by this priority:
  1. `"yanked"`  — if its `yanked` field is `true`;
  2. `"prerelease"` — else, if it carries a pre-release suffix;
  3. `"older"` — otherwise (a stable, non-yanked version below `latest_stable`).

* **Reclaimable** artefacts are the superseded entries whose `reason` is `"older"` or
  `"yanked"` (pre-releases are retained for testing and are **never** counted as
  reclaimable).

## Required output #1 — `/home/user/reports/upgrade_plan.json`

Create the directory `/home/user/reports` (mode `755`) if it does not exist, then write a
**minified** JSON document (no spaces, no extra newlines — only a single trailing `\n`).
Keys MUST appear in **exactly** this order:

```json
{
  "registry": "/home/user/registry",
  "generated_at": "<RFC-3339 UTC, e.g. 2024-05-01T12:00:00Z>",
  "packages": [
    {
      "name": "<package>",
      "candidates_considered": <total number of versions for this package>,
      "latest_stable": "<version>",
      "superseded": [
        { "version": "<version>", "reason": "<older|prerelease|yanked>", "size_bytes": <int> }
      ],
      "reclaimable_bytes": <sum of size_bytes over reclaimable entries of this package>
    }
  ],
  "total_reclaimable_bytes": <sum of every package's reclaimable_bytes>
}
```

Rules:

* `generated_at` MUST be a real RFC-3339 UTC timestamp `YYYY-MM-DDThh:mm:ssZ`.
* The `packages` array MUST be sorted **alphabetically** by `name`.
* Within each package, the `superseded` array MUST be sorted by SemVer precedence in
  **ascending** order (lowest precedence first).
* The whole document is minified using `,` and `:` separators (no whitespace), e.g.
  `{"registry":"/home/user/registry",...}`.

## Required output #2 — `/home/user/reports/upgrade_plan.log`

A plain-text log with **one line per package** (packages alphabetical) followed by a final
total line. Every line ends with `\n`. Use this exact format:

```
<package> keep <latest_stable> reclaim <reclaimable_bytes> bytes from <k> artefact(s)
```

where `<k>` is the number of reclaimable entries for that package. After all package lines,
append exactly:

```
TOTAL reclaimable <total_reclaimable_bytes> bytes
```

## Done criteria

Both files must exist with the exact byte content specified above (only `generated_at`'s
value may differ). An automated grader recomputes the correct plan from the registry and
compares it against your files.
