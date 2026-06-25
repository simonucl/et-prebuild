# Repair the Offline Maven Repository

You are preparing an air-gapped Maven repository handoff for:

- groupId: `com.acme`
- artifactId: `edge-policy-runtime`
- version: `2.4.1`

The source payload is staged under `/app/maven-src`, and the broken repository is staged under:

`/app/repo/com/acme/edge-policy-runtime`

Repair the repository in place. Do not use the network and do not modify anything under `/app/maven-src`.

The final artifact directory `/app/repo/com/acme/edge-policy-runtime/2.4.1` must contain exactly these files:

- `edge-policy-runtime-2.4.1.jar`
- `edge-policy-runtime-2.4.1.jar.md5`
- `edge-policy-runtime-2.4.1.jar.sha1`
- `edge-policy-runtime-2.4.1.jar.sha256`
- `edge-policy-runtime-2.4.1.pom`
- `edge-policy-runtime-2.4.1.pom.md5`
- `edge-policy-runtime-2.4.1.pom.sha1`
- `edge-policy-runtime-2.4.1.pom.sha256`

Create `/app/repo/com/acme/edge-policy-runtime/maven-metadata.xml` and its `.md5`, `.sha1`, and `.sha256` checksum files.

JAR requirements:

- It must be a ZIP/JAR file with no directory entries.
- It must contain exactly these members in this order:
  1. `META-INF/MANIFEST.MF`
  2. `com/acme/edgepolicy/Runtime.class`
  3. `com/acme/edgepolicy/schema.json`
  4. `LICENSE.txt`
- Use deflated compression for every member.
- Normalize each member timestamp to `1980-01-01 00:00:00`.
- Store Unix regular-file mode `0644` for every member.
- `META-INF/MANIFEST.MF` content must be exactly:

```text
Manifest-Version: 1.0
Implementation-Title: edge-policy-runtime
Implementation-Version: 2.4.1
Built-By: terminal-rsi

```

Use CRLF line endings in the manifest, including the final blank line. The other JAR members must come byte-for-byte from `/app/maven-src`.

The POM must describe this artifact with Maven's `4.0.0` model, groupId `com.acme`, artifactId `edge-policy-runtime`, version `2.4.1`, packaging `jar`, name `Acme Edge Policy Runtime`, and license `Apache-2.0`.

The Maven metadata file must list only version `2.4.1`, with `latest` and `release` both set to `2.4.1` and `lastUpdated` set to `20260625000000`.

Each checksum sidecar must contain the lowercase hex digest of the corresponding file bytes followed by exactly one newline. Remove stale files from the artifact directory and from `/app/repo/com/acme/edge-policy-runtime`.
