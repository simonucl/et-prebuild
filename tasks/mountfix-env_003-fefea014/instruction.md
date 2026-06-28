# Offline stale asset reporter

You are maintaining `/home/user/reconcilor`, a small Python project that should expose a console command named `stale-report`.

The project currently has bugs in its packaging metadata and CLI implementation. Fix the project so it can be installed offline with `python3 -m pip install -e .` and then run as:

```bash
stale-report --data-dir /home/user/reconcilor/data --output-dir /home/user/reconcilor/out --as-of 2024-04-15
```

The command must read:

- `inventory.csv`, with columns `path,owner,last_seen,classification`
- `checksums.sha256`, in normal `sha256sum` format: `<64 hex characters><two spaces><relative path>`. Blank lines and lines beginning with `#` must be ignored.

An inventory row is stale using these retention rules:

- `prod`: stale when age is greater than 90 days
- `archive`: stale when age is greater than 365 days
- `ephemeral`: never stale
- any other classification: stale when age is greater than 180 days

Age is the number of calendar days from `last_seen` through the supplied `--as-of` date. Do not modify files under `data/`.

The command must create the output directory if needed and write exactly these two files:

```text
/home/user/reconcilor/out/stale_manifest.json
/home/user/reconcilor/out/stale_manifest.tsv
```

`stale_manifest.json` must be minified JSON with a single trailing newline. Its top-level keys must appear in this order:

```json
{"as_of":"2024-04-15","summary":{"stale_count":0,"missing_checksum_count":0,"owners":[]},"stale_assets":[]}
```

For real data, `stale_assets` contains objects with keys in this order:

```json
{"path":"...","owner":"...","last_seen":"YYYY-MM-DD","classification":"prod","age_days":123,"sha256":"..."}
```

Use JSON `null` for `sha256` when a stale asset has no checksum entry. Sort `stale_assets` by `owner` alphabetically, then by `path` alphabetically. `summary.owners` must be the sorted unique owners represented in the stale list.

`stale_manifest.tsv` must have this header and one line per stale asset in the same order as the JSON:

```text
owner	path	age_days	classification	sha256
```

Use the literal string `MISSING` in the TSV when a stale asset has no checksum. End the TSV with a trailing newline.
