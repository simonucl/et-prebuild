# Deterministic Java JAR Handoff

You are preparing an offline release handoff for the Java utility `log-scrubber` version `1.2.0`.

The source tree is already staged at:

`/home/user/jar_lab/src`

Replace the stale contents of:

`/home/user/jar_lab/dist`

Do not use the network, and do not modify anything under `/home/user/jar_lab/src`.

Required final state:

1. `/home/user/jar_lab/dist` must contain exactly these three files:
   - `log-scrubber-1.2.0.jar`
   - `log-scrubber-1.2.0.pom`
   - `SHA256SUMS`

2. `log-scrubber-1.2.0.jar` must be an executable JAR built from the staged Java sources.
   - It must run with `java -jar /home/user/jar_lab/dist/log-scrubber-1.2.0.jar`.
   - Its manifest must set `Main-Class: com.acme.scrub.Main`.
   - It must include the service provider file from `src/META-INF/services`.
   - It must include the default rule resource from `src/com/acme/scrub/rules/default-rules.txt`.
   - It must not include `.java` source files, directory entries, temporary files, or any stale `dist` content.

3. The JAR must be deterministic.
   - Archive members must appear in this exact order:
     - `META-INF/MANIFEST.MF`
     - `META-INF/services/com.acme.scrub.Scrubber`
     - `com/acme/scrub/Main.class`
     - `com/acme/scrub/Redactor.class`
     - `com/acme/scrub/Scrubber.class`
     - `com/acme/scrub/rules/default-rules.txt`
   - Every member must use ZIP deflate compression.
   - Every member timestamp must be `2024-05-06 07:08:10`.
   - Every stored Unix permission must be `0644`.

4. `log-scrubber-1.2.0.pom` must be a Maven POM XML file for:
   - group id `com.acme`
   - artifact id `log-scrubber`
   - version `1.2.0`
   - name `log-scrubber`
   - description `Offline log redaction utility`

5. `SHA256SUMS` must contain exactly two lines in this order:

```text
<sha256 of log-scrubber-1.2.0.jar>  log-scrubber-1.2.0.jar
<sha256 of log-scrubber-1.2.0.pom>  log-scrubber-1.2.0.pom
```

All generated text files must end with exactly one trailing newline. All work must stay under `/home/user/jar_lab`.
