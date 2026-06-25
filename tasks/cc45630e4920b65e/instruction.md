# Build the Offline rsync Batch Handoff

The release engineer has staged two local site trees:

- Baseline receiver copy: `/home/user/rsync-lab/baseline/site`
- Desired final site: `/home/user/rsync-lab/desired/site`

The current receiver tree is at `/home/user/rsync-lab/receiver/site`.

Create a self-contained offline handoff in `/home/user/rsync-lab/handoff` that can transform any clean copy of the baseline receiver tree into the desired tree without reading from `/home/user/rsync-lab/desired`.

Required end state:

1. `/home/user/rsync-lab/handoff` must contain exactly these four files:
   - `site-update.batch`
   - `apply-site-update.sh`
   - `itemized-changes.txt`
   - `manifest.json`

2. Generate the batch with real rsync batch mode from the desired site into the receiver site using archive mode, deletion, checksum comparison, and itemized changes. The intended option set is:

   ```bash
   rsync -a --delete --checksum --itemize-changes --write-batch=...
   ```

3. `itemized-changes.txt` must contain the itemized change output from that batch generation.

4. `apply-site-update.sh` must be executable and relocatable. It must locate `site-update.batch` next to itself and apply it to the destination directory passed as its first argument using rsync read-batch mode. It must not hard-code `/home/user/rsync-lab` or read from the desired tree.

5. Applying the handoff to a clean baseline copy must reproduce the desired tree exactly, including removed files, symlinks, executable bits, regular file modes, and file contents.

6. Write `/home/user/rsync-lab/handoff/manifest.json` as minified JSON with exactly one trailing newline. The top-level keys must appear in this order:

   `batch`, `apply_script`, `source_root`, `options`, `changes`, `batch_sha256`

   Use these values:
   - `batch`: `site-update.batch`
   - `apply_script`: `apply-site-update.sh`
   - `source_root`: `site/`
   - `options`: `["-a","--delete","--checksum","--itemize-changes"]`
   - `changes`: the itemized change lines as strings, in file order
   - `batch_sha256`: the lowercase SHA-256 hex digest of the final `site-update.batch`

Do not modify `/home/user/rsync-lab/baseline/site` or `/home/user/rsync-lab/desired/site`.
