# SemVer artifact ledger — full precedence ordering

You are the release engineer for an on-premise package registry. A flat directory of build
artifacts has accumulated and you must produce a single machine-readable ledger that, **for
every package**, lists *all* of its valid versions in strict
**Semantic Versioning 2.0.0** precedence order (https://semver.org/spec/v2.0.0.html). Naive
string sorting will produce the wrong order and fail the automated checker.

## Input (read-only — do NOT modify, move, rename, or delete anything here)

    /home/user/registry/artifacts

It contains only regular files, each named exactly:

    <name>@<version>.bin

where:

* `<name>` is a lower-case identifier that contains **no `@`**.
* `<version>` is the raw version string (everything between the `@` and the trailing `.bin`).
  Some version strings are **not** valid SemVer 2.0.0 and must be quarantined (see below).

## What you must produce

Write a JSON file to **`/home/user/report.json`** with this exact structure:

```json
{
  "registry": "/home/user/registry/artifacts",
  "packages": [
    {
      "name": "<package name>",
      "latest": "<highest-precedence valid version string>",
      "ordered": ["<v1>", "<v2>", "..."],
      "count": <number of valid versions for this package>
    }
  ],
  "quarantined": ["<name>@<rawversion>", "..."]
}
```

### Rules

1. **Validity.** A version is valid only if it matches the SemVer 2.0.0 grammar exactly:
   `MAJOR.MINOR.PATCH`, each a non-negative integer with **no leading zeros**, optionally
   followed by a `-<prerelease>` part and/or a `+<build>` part using only the identifiers
   the spec allows. Anything that does not match (e.g. `1.0`, `v2.0.0`, `01.0.0`, `1.0.0-`,
   `1.0.0-alpha..1`) is **invalid**.

2. **Quarantine.** Every invalid artifact contributes one entry `"<name>@<rawversion>"` to
   the top-level `quarantined` array (the raw string exactly as it appears in the file name,
   with the trailing `.bin` removed). Sort `quarantined` in **ascending** plain lexicographic
   (byte/ASCII) order.

3. **Packages.** A package appears in `packages` **only if it has at least one valid
   version**. Sort `packages` by `name` in ascending plain lexicographic order. A package
   whose every version is invalid must NOT appear in `packages` (only in `quarantined`).

4. **`ordered`.** The list of that package's valid version strings (exactly as they appear,
   including any `+build` metadata) sorted by SemVer precedence in **descending** order
   (highest precedence first). Precedence follows SemVer 2.0.0 §11:
   * Compare major, then minor, then patch numerically.
   * A version **with** a pre-release has **lower** precedence than the same version without.
   * Compare pre-release identifiers left-to-right: numeric identifiers compared numerically,
     alphanumeric identifiers compared by ASCII order, a numeric identifier always ranks
     **lower** than an alphanumeric one, and a larger set of pre-release fields ranks higher
     when all preceding fields are equal.
   * **Build metadata is ignored for precedence.** Therefore two versions that differ only in
     their `+build` metadata have **equal** precedence. When (and only when) two versions
     compare equal in precedence, break the tie by ordering them by their **raw version
     string in ascending** plain lexicographic order.

5. **`latest`.** The first element of `ordered` (the single highest-precedence valid version).

6. **`count`.** The number of valid versions for that package (the length of `ordered`).

Only the structure and values matter — formatting/whitespace of the JSON is not graded, but
the **order of every array is significant** and is checked.
