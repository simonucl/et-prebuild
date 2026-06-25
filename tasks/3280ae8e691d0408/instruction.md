# Publish a Deterministic Maven Repository Artifact

Prepare the offline Maven repository under `/app/maven-repo` from the staged payload in `/app/staging`.

Publish `com.acme:telemetry-core:2.7.1` using Maven's default repository path:

`/app/maven-repo/com/acme/telemetry-core/2.7.1/`

The version directory must contain exactly these files:

- `telemetry-core-2.7.1.jar`
- `telemetry-core-2.7.1.jar.md5`
- `telemetry-core-2.7.1.jar.sha1`
- `telemetry-core-2.7.1.jar.sha256`
- `telemetry-core-2.7.1.pom`
- `telemetry-core-2.7.1.pom.md5`
- `telemetry-core-2.7.1.pom.sha1`
- `telemetry-core-2.7.1.pom.sha256`

The artifact directory `/app/maven-repo/com/acme/telemetry-core/` must contain exactly the `2.7.1` directory plus:

- `maven-metadata.xml`
- `maven-metadata.xml.md5`
- `maven-metadata.xml.sha1`
- `maven-metadata.xml.sha256`

Build `telemetry-core-2.7.1.jar` from `/app/staging/classes`. It must be a deterministic JAR/ZIP with these entries in this exact order:

1. `META-INF/MANIFEST.MF`
2. `com/acme/telemetry/Collector.class`
3. `com/acme/telemetry/internal/Envelope.class`
4. `META-INF/services/com.acme.telemetry.Plugin`

Use DEFLATED compression. Every ZIP member timestamp must be `1980-01-01 00:00:00`, every member must use Unix metadata, and every member must have mode `0644`.

The manifest content must be exactly:

```text
Manifest-Version: 1.0
Created-By: terminal-rsi
Implementation-Title: telemetry-core
Implementation-Version: 2.7.1

```

Copy `/app/staging/pom.xml` byte-for-byte to `telemetry-core-2.7.1.pom`.

Write `maven-metadata.xml` as UTF-8 text with exactly this content and one trailing newline:

```xml
<metadata>
  <groupId>com.acme</groupId>
  <artifactId>telemetry-core</artifactId>
  <versioning>
    <release>2.7.1</release>
    <versions>
      <version>2.7.1</version>
    </versions>
    <lastUpdated>20260625000000</lastUpdated>
  </versioning>
</metadata>
```

For the JAR, POM, and `maven-metadata.xml`, create checksum sidecar files for MD5, SHA-1, and SHA-256. Each checksum file must contain only the lowercase hex digest followed by exactly one newline.

Do not leave stale or extra files anywhere under `/app/maven-repo/com/acme/telemetry-core`.
