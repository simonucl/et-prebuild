# Repair the Offline npm Package Handoff

You are preparing the final offline npm handoff for the CLI package staged at:

`/home/user/npm-lab/src/acme-logship`

The source tree is intentionally broken. Repair it and create the final package artifacts without using the network.

Required end state:

1. The source package manifest at `/home/user/npm-lab/src/acme-logship/package.json` must describe the package exactly as:

```json
{
  "name": "@acme/logship",
  "version": "0.6.0",
  "description": "Offline log shipping CLI",
  "license": "MIT",
  "bin": {
    "logship": "bin/logship.js"
  },
  "files": [
    "bin/",
    "lib/",
    "README.md",
    "LICENSE"
  ]
}
```

2. `/home/user/npm-lab/src/acme-logship/bin/logship.js` must be executable and must keep its existing shebang.

3. `/home/user/npm-lab/src/acme-logship/lib/index.js` must export `formatLine(level, message)` so that running:

```bash
node /home/user/npm-lab/src/acme-logship/bin/logship.js warn "disk low"
```

prints exactly:

```text
{"level":"warn","message":"disk low"}
```

with one trailing newline.

4. Create `/home/user/npm-lab/dist/acme-logship-0.6.0.tgz` by packing the repaired source package with the real npm CLI.

5. Capture the corresponding `npm pack --json` output for that packed artifact at `/home/user/npm-lab/dist/packument.json`.

Do not copy `notes/private-release-notes.txt` into the package. Do not rename the staged source directory.
