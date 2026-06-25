# Offline npm Package Handoff

You are preparing an offline handoff for the scoped npm CLI package staged at:

`/home/user/work/route-lens`

The source tree is intentionally not ready for publication. Repair the package metadata, preserve the source files, and produce the release artifacts in:

`/home/user/handoff`

## Required source repair

Update `/home/user/work/route-lens/package.json` to this exact minified JSON content:

```json
{"name":"@acme/route-lens","version":"2.1.0","description":"CLI for normalizing and listing route paths before edge-router deploys.","license":"MIT","type":"commonjs","main":"lib/index.js","bin":{"route-lens":"bin/route-lens.js"},"files":["bin/","lib/","README.md","LICENSE"],"scripts":{"test":"node test/smoke.js"}}
```

Set `/home/user/work/route-lens/bin/route-lens.js` executable by its owner, group, and others. Do not change the contents of the JavaScript, README, LICENSE, test fixture, docs, or tmp files.

## Required handoff artifacts

Create `/home/user/handoff` containing exactly these two files and no others:

1. `acme-route-lens-2.1.0.tgz`
   - Generate this tarball from `/home/user/work/route-lens` using npm's package packing behavior.
   - The tarball must include only the package files selected by the repaired package metadata.

2. `pack-manifest.json`
   - Run npm's JSON pack output for the package and write a single minified JSON object.
   - The object must contain the key `source` first with value `/home/user/work/route-lens`.
   - After `source`, include npm's pack metadata keys and values for this tarball in the same order npm reports them for the single packed package.
   - Do not write the outer JSON array that npm prints.
   - Do not add a trailing newline.

The final artifacts must be reproducible from the repaired source tree without network access.
