# Repair the Offline NuGet v3 Feed

You are preparing an offline NuGet v3 feed for the package `Acme.EdgeRules` version `1.4.0`.

The source package files are staged under:

`/app/nuget-src`

The broken feed is staged under:

`/app/nuget-feed/v3`

Do not use the network. Replace the stale feed content with a deterministic NuGet package and matching feed metadata.

Required final files:

1. `/app/nuget-feed/v3/index.json`
2. `/app/nuget-feed/v3/flatcontainer/acme.edgerules/index.json`
3. `/app/nuget-feed/v3/flatcontainer/acme.edgerules/1.4.0/acme.edgerules.1.4.0.nupkg`
4. `/app/nuget-feed/v3/flatcontainer/acme.edgerules/1.4.0/acme.edgerules.nuspec`
5. `/app/nuget-feed/v3/registration/acme.edgerules/index.json`

The package path must use NuGet's lowercase flat-container convention for package id and version.

Build `acme.edgerules.1.4.0.nupkg` as a real ZIP/NuGet package containing exactly these members, in this order, with no directory entries:

1. `[Content_Types].xml`
2. `_rels/.rels`
3. `Acme.EdgeRules.nuspec`
4. `lib/net8.0/Acme.EdgeRules.dll`
5. `buildTransitive/Acme.EdgeRules.props`
6. `README.md`
7. `LICENSE.txt`

Package requirements:

- Use deflate compression for every member.
- Set every member timestamp to `2024-05-06 07:08:10`.
- Store Unix mode `0644` for every member.
- Copy the DLL, props file, README, and license byte-for-byte from `/app/nuget-src`.
- The `.nuspec` member and sidecar `acme.edgerules.nuspec` must be identical bytes.

The `.nuspec` must be compact XML with this metadata:

- id: `Acme.EdgeRules`
- version: `1.4.0`
- authors: `Acme Platform`
- description: `Offline edge routing rule helpers for Acme gateways.`
- repository type: `git`
- repository url: `https://git.example.invalid/acme/edge-rules`
- repository commit: `8f3d2ac91b7e`
- license file: `LICENSE.txt`
- readme: `README.md`
- package type: `Dependency`
- dependency group target framework: `net8.0`, with no dependency entries

Create the NuGet v3 service index and registration metadata as compact single-line JSON files with exactly one trailing newline. The registration metadata must describe the final package, include a SHA-512 package hash encoded with standard base64, use `packageHashAlgorithm` value `SHA512`, and point `packageContent` at the flat-container `.nupkg` path.

When finished, there must be no stale versions or extra regular files under `/app/nuget-feed/v3`.
