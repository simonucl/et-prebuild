# Offline Git Release Handoff

You are preparing an offline handoff for `edge-collector` version `v1.9.0`.

The source repository is staged at:

`/home/user/release/source`

The receiving team has only the base repository at:

`/home/user/release/receiver.git`

It already contains `main` and tag `v1.8.0`, but it does not contain the `release/v1.9` branch or the `v1.9.0` tag.

Create the final handoff under:

`/home/user/release/handoff`

Required end state:

1. Create an incremental Git bundle:

   `/home/user/release/handoff/edge-collector-v1.9.0.bundle`

   The bundle must expose exactly these refs:

   - `refs/heads/release/v1.9`
   - `refs/tags/v1.9.0`

   It must be based on `v1.8.0` as the prerequisite, so it verifies against `/home/user/release/receiver.git` but is not a standalone full-repository bundle.

2. Create binary-capable patch files from the exact range `v1.8.0..release/v1.9` in:

   `/home/user/release/handoff/patches`

   Use Git's format-patch output with full object indexes and binary patch support. Keep Git's generated patch filenames.

3. Create a minified manifest at:

   `/home/user/release/handoff/manifest.json`

   It must contain one JSON object with these keys in this exact order:

   `schema_version`, `project`, `base_tag`, `base_commit`, `target_ref`, `target_tag`, `target_commit`, `bundle`, `patches`, `archive`

   Values:

   - `schema_version`: `1`
   - `project`: `"edge-collector"`
   - `base_tag`: `"v1.8.0"`
   - `base_commit`: commit id for `v1.8.0`
   - `target_ref`: `"refs/heads/release/v1.9"`
   - `target_tag`: `"v1.9.0"`
   - `target_commit`: commit id for `release/v1.9`
   - `bundle`: object with `path` and `sha256` for `edge-collector-v1.9.0.bundle`
   - `patches`: array of objects, one per patch in filename order, each with `path` and `sha256`
   - `archive`: object with `path` equal to `edge-collector-v1.9.0-handoff.tar.gz` and `file_count` equal to the number of non-directory files inside the archive

   The JSON must be compact with no extra spaces and exactly one trailing newline.

4. Create the normalized tarball:

   `/home/user/release/handoff/edge-collector-v1.9.0-handoff.tar.gz`

   It must contain a single top-level directory named `edge-collector-v1.9.0-handoff/`, with the bundle, `manifest.json`, and the `patches/` directory inside it. Normalize the tar entries to numeric owner/group `0/0`, directory mode `0755`, file mode `0644`, and mtime `2024-04-01T00:00:00Z`. The gzip header must not store an original filename or timestamp.

Do not modify the source repository history or the receiver repository. Do not use the network.
