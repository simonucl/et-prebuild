# Deterministic Offline Wheel and Simple Index Handoff

You are preparing a sealed, offline Python package handoff for:

`acme-ledger-export` version `0.4.2`

The source tree is already staged at:

`/home/user/wheel_lab/src`

Replace the stale artifacts under `/home/user/wheel_lab` without using the network.

Required end state:

1. `/home/user/wheel_lab/dist` must contain exactly two files:
   - `acme_ledger_export-0.4.2-py3-none-any.whl`
   - `SHA256SUMS`

2. The wheel must be a valid Python wheel containing exactly these members, in this order, with no directory entries:
   - `acme_ledger_export/__init__.py`
   - `acme_ledger_export/cli.py`
   - `acme_ledger_export/schemas/default.json`
   - `acme_ledger_export-0.4.2.dist-info/METADATA`
   - `acme_ledger_export-0.4.2.dist-info/WHEEL`
   - `acme_ledger_export-0.4.2.dist-info/entry_points.txt`
   - `acme_ledger_export-0.4.2.dist-info/RECORD`

3. The first three wheel members must exactly match the source files under `/home/user/wheel_lab/src`. Do not package editor backups, temporary notes, `pyproject.toml`, or directory entries.

4. Use these metadata file contents exactly:

`METADATA`
```text
Metadata-Version: 2.1
Name: acme-ledger-export
Version: 0.4.2
Summary: Offline ledger export normalizer
Requires-Python: >=3.10
```

`WHEEL`
```text
Wheel-Version: 1.0
Generator: terminal-rsi
Root-Is-Purelib: true
Tag: py3-none-any
```

`entry_points.txt`
```text
[console_scripts]
ledger-export = acme_ledger_export.cli:main
```

5. Normalize the wheel archive:
   - every member is deflated, not stored
   - every member has zip permission `0644`
   - every member timestamp is `2024-02-29 12:00:00`
   - every text metadata file ends with one newline

6. `RECORD` must be valid wheel CSV. It must list every preceding wheel member in the same order with `sha256=<urlsafe-base64-no-padding-digest>` and byte size, then list `acme_ledger_export-0.4.2.dist-info/RECORD,,` as the final row.

7. `SHA256SUMS` must contain exactly one line:

```text
<hex sha256 of the wheel><two spaces>acme_ledger_export-0.4.2-py3-none-any.whl
```

8. Create `/home/user/wheel_lab/simple/acme-ledger-export/index.html` as a minimal offline simple-index page. It must contain exactly:

```html
<!DOCTYPE html>
<html>
  <body>
    <a href="../../dist/acme_ledger_export-0.4.2-py3-none-any.whl#sha256=<hex sha256 of the wheel>">acme_ledger_export-0.4.2-py3-none-any.whl</a>
  </body>
</html>
```

Leave the source tree in place. Only replace the handoff artifacts.
