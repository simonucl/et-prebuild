# Repair the Offline Conda Noarch Channel

You are preparing an offline Conda channel handoff for a small noarch Python package named `acme-tokens` version `0.4.0`.

The staged source files are under:

`/home/user/conda_lab/src`

The channel root is:

`/home/user/conda_lab/channel`

Do not use the network, and do not modify, delete, move, or rename any file under `/home/user/conda_lab/src`.

Required end state:

1. Replace the stale channel contents so `/home/user/conda_lab/channel/noarch` contains exactly these files:
   - `acme-tokens-0.4.0-py_0.tar.bz2`
   - `current_repodata.json`
   - `repodata.json`

2. Create `/home/user/conda_lab/channel/channeldata.json`.

3. The package must be a real Conda-style `.tar.bz2` archive. It must contain exactly these members in this order, with no directory entries:

```text
info/index.json
info/files
info/paths.json
site-packages/acme_tokens/__init__.py
site-packages/acme_tokens/cli.py
python-scripts/acme-tokens
```

4. Package archive metadata must be normalized:
   - every member mtime is `2026-06-25 00:00:00 UTC`
   - uid and gid are `0`
   - uname and gname are empty
   - `python-scripts/acme-tokens` has mode `0755`
   - every other member has mode `0644`

5. Package content requirements:
   - `site-packages/acme_tokens/__init__.py` and `site-packages/acme_tokens/cli.py` must match the corresponding source files exactly.
   - `python-scripts/acme-tokens` must be an executable Python script that calls `acme_tokens.cli.main`.
   - `info/index.json`, `info/paths.json`, `repodata.json`, `current_repodata.json`, and `channeldata.json` must be minified JSON with exactly one trailing newline.
   - `info/files` must list the three installed runtime files, one per line, in package order, with exactly one trailing newline:

```text
site-packages/acme_tokens/__init__.py
site-packages/acme_tokens/cli.py
python-scripts/acme-tokens
```

6. `info/index.json` must describe the package with this identity:
   - name: `acme-tokens`
   - version: `0.4.0`
   - build: `py_0`
   - build number: `0`
   - subdir: `noarch`
   - noarch type: `python`
   - license: `MIT`
   - timestamp: `1782345600000`
   - dependency: `python >=3.10`

7. `info/paths.json` must use Conda paths format version `1` and include entries for the three runtime files in package order. Each entry must include `_path`, `path_type` set to `hardlink`, `sha256`, and `size_in_bytes`, computed from the bytes stored in the package.

8. `repodata.json` and `current_repodata.json` must both describe the noarch subdir. They must include one package record for `acme-tokens-0.4.0-py_0.tar.bz2` containing the package identity above plus the final package `md5`, `sha256`, and byte `size`. `current_repodata.json` may be the same complete package set as `repodata.json`.

9. `channeldata.json` must be minified JSON with one package entry for `acme-tokens`, summary `Offline token normalizer`, license `MIT`, version `0.4.0`, and subdirs `["noarch"]`.

10. Installing by extracting the package into a temporary prefix and running `python-scripts/acme-tokens` with `PYTHONPATH` pointed at that prefix's `site-packages` must work offline.

Remove stale package and metadata files from the channel. All final work must stay under `/home/user/conda_lab`.
