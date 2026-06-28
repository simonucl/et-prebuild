# PEP 440 Version Resolver

You are a Python release engineer. A dependency-audit pipeline has dropped a small
workspace at `/home/user/work`. For every package it lists a **version specifier** and a
catalogue of **candidate version strings** (some of them malformed). Your job is to resolve,
per package, which candidates are valid, sort them, and pick the best installable version —
following the **PEP 440** version-identification and version-specifier rules **exactly**.

The grader compares your output **byte-for-byte**, so obey every formatting rule precisely.

## Inputs (read-only — do not modify)

### `/home/user/work/packages.txt`
One package per line:

```
<name> <specifier>
```

* `<name>` is the package name (no spaces).
* `<specifier>` is everything after the first run of whitespace — a PEP 440 specifier set
  such as `>=3.0,<4.0,!=3.1.*`, `~=2.2`, or `===1.5.0`. A line may have **no** specifier
  (name only), which means "match every valid candidate".
* Blank lines are ignored.

### `/home/user/work/candidates/<name>.txt`
For each package, one candidate version string per line. Strip leading/trailing whitespace
from each line. **Blank lines (after stripping) are ignored entirely** — they count as
neither valid nor invalid. The remaining stripped strings are the candidates.

## What "valid" means (PEP 440)

A candidate is **valid** if it parses as a PEP 440 version identifier (epochs `N!`,
release segments, pre-releases `aN`/`bN`/`rcN`, post-releases `.postN`, dev-releases
`.devN`, and local versions `+label` are all permitted; surrounding `v`/whitespace and
case/separator variants are normalised). Otherwise it is **invalid**.

For every valid candidate you must use its **normalised** canonical form (e.g.
`3.2.0_alpha1` → `3.2.0a1`, `2.0.0-rc1` → `2.0.0rc1`, `01.2.3` → `1.2.3`).

## What to compute, per package

* `valid`   — the normalised forms of all valid candidates, **sorted ascending by PEP 440
  precedence**. If two valid candidates compare **equal** under PEP 440 (e.g. `1.5`,
  `1.5.0`, `1.5.0.0`), keep them in their **order of first appearance** in the candidate
  file (stable order). One entry per candidate line (do **not** de-duplicate equal versions).
* `invalid` — the malformed candidate strings (stripped, original spelling), in the **order
  they appear** in the file.
* `best` — the **highest** valid candidate (PEP 440 order) that **satisfies the specifier**,
  with **pre-releases allowed** during matching. Output its normalised form, or JSON `null`
  if nothing satisfies the specifier. (PEP 440 specifier semantics apply in full, including
  `~=`, `==X.*`/`!=X.*` prefix matching, exclusive `<`/`>` pre-release rules, and `===`
  arbitrary string equality.)
* `best_stable` — like `best`, but restricted to versions that are **not** pre-releases and
  **not** dev-releases (post-releases and local versions count as stable). `null` if none.
* `count_valid` / `count_invalid` — the number of valid / invalid candidates.

## Output — `/home/user/work/out/resolution.json`

Create the directory `/home/user/work/out` and write a single JSON object as **one line of
minified JSON** (no spaces after `,` or `:`) followed by a **single trailing newline**.

Use **exactly** these keys, in **exactly** this order, with packages sorted by `name`
(ASCII ascending):

```
{"tool":"pep440-resolver/v1","packages":[{"name":...,"valid":[...],"invalid":[...],"best":...,"best_stable":...,"count_valid":N,"count_invalid":M}, ...],"summary":{"packages":P,"valid":TV,"invalid":TI,"resolved":R}}
```

* `summary.packages` — number of packages.
* `summary.valid` / `summary.invalid` — totals across all packages.
* `summary.resolved` — number of packages whose `best` is non-null.

Do not modify anything under `/home/user/work/packages.txt` or
`/home/user/work/candidates/`. Only create `/home/user/work/out/resolution.json`.
