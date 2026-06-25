# Offline npm Package Handoff

You are preparing the final offline package handoff for the scoped npm package staged at:

`/home/user/npm-lab/stream-redactor`

The package source is already present and its runtime code should not need to be rewritten. The handoff metadata is not ready.

Your required end state is:

1. Repair `/home/user/npm-lab/stream-redactor/package.json` so that these fields are exactly correct:
   - `name`: `@acme/stream-redactor`
   - `version`: `1.2.3`
   - `main`: `index.js`
   - `bin`: an object mapping `stream-redactor` to `cli.js`
   - `files`: exactly this array, in this order:
     `["index.js","cli.js","rules/default.json","README.md","LICENSE"]`

2. Create `/home/user/npm-lab/dist` if needed, and use the real npm packaging tool to pack the repaired source tree into that directory.

3. The final tarball must be:

   `/home/user/npm-lab/dist/acme-stream-redactor-1.2.3.tgz`

   Remember that npm uses a de-scoped filename for scoped packages.

4. Create `/home/user/npm-lab/dist/pack-manifest.json`.
   It must be a minified single JSON object followed by one trailing newline, with keys in this exact order:

   ```json
   {"name":"@acme/stream-redactor","version":"1.2.3","filename":"acme-stream-redactor-1.2.3.tgz","shasum":"...","integrity":"...","files":["..."]}
   ```

   Populate `filename`, `shasum`, `integrity`, and `files` from the actual `npm pack --json` result for the final tarball. The `files` array should contain only the path strings reported by npm, in npm's reported order.

Do not copy source files into `dist` by hand. The handoff should contain exactly the `.tgz` package and `pack-manifest.json`.
