# Repair the Offline Maven2 Repository

Repair the Maven repository rooted at `/app/repo` for:

- groupId: `com.acme`
- artifactId: `telemetry-agent`
- version: `2.4.1`

The staged inputs are under `/app/staging`. Rebuild the repository directory:

`/app/repo/com/acme/telemetry-agent`

The final repository must contain exactly these files:

- `maven-metadata.xml`
- `maven-metadata.xml.sha1`
- `maven-metadata.xml.md5`
- `2.4.1/telemetry-agent-2.4.1.jar`
- `2.4.1/telemetry-agent-2.4.1.jar.sha1`
- `2.4.1/telemetry-agent-2.4.1.jar.md5`
- `2.4.1/telemetry-agent-2.4.1-sources.jar`
- `2.4.1/telemetry-agent-2.4.1-sources.jar.sha1`
- `2.4.1/telemetry-agent-2.4.1-sources.jar.md5`
- `2.4.1/telemetry-agent-2.4.1.pom`
- `2.4.1/telemetry-agent-2.4.1.pom.sha1`
- `2.4.1/telemetry-agent-2.4.1.pom.md5`

Build `telemetry-agent-2.4.1.jar` from the staged class/resource files and `LICENSE.txt`. Its ZIP entries must be deterministic, root-relative, and ordered as:

1. `META-INF/`
2. `META-INF/MANIFEST.MF`
3. `META-INF/services/`
4. `META-INF/services/com.acme.telemetry.Plugin`
5. `com/`
6. `com/acme/`
7. `com/acme/telemetry/`
8. `com/acme/telemetry/Agent.class`
9. `com/acme/telemetry/internal/`
10. `com/acme/telemetry/internal/Config.class`
11. `LICENSE.txt`

The manifest content must be:

```text
Manifest-Version: 1.0
Created-By: terminal-rsi
Build-Jdk-Spec: 17

```

Build `telemetry-agent-2.4.1-sources.jar` from the staged Java source files and `LICENSE.txt`, also with deterministic ZIP metadata, ordered as:

1. `META-INF/`
2. `META-INF/MANIFEST.MF`
3. `com/`
4. `com/acme/`
5. `com/acme/telemetry/`
6. `com/acme/telemetry/Agent.java`
7. `com/acme/telemetry/internal/`
8. `com/acme/telemetry/internal/Config.java`
9. `LICENSE.txt`

For both JARs, directory entries should be directories, all entries should use the timestamp `1980-01-01T00:00:00`, and regular file entries should have non-executable read permissions.

Copy the staged POM to `2.4.1/telemetry-agent-2.4.1.pom` exactly.

Write `maven-metadata.xml` for this single released version with `lastUpdated` set to `20260102030405`.

For every `.jar`, `.pom`, and `maven-metadata.xml` file you create, write matching lowercase hex `.sha1` and `.md5` checksum sidecar files containing only the digest and one trailing newline.
