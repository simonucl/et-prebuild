# Rebuild the Multi-Release Java JAR

You are preparing the offline release handoff for `diag-probe` version `1.2.0`.

The source tree is already staged at:

```text
/home/user/jar_lab/src/base
/home/user/jar_lab/src/java11
```

Replace the stale artifact at:

```text
/home/user/jar_lab/dist/diag-probe-1.2.0.jar
```

Required end state:

1. The JAR is executable with `java -jar /home/user/jar_lab/dist/diag-probe-1.2.0.jar`.
2. It is a real Java multi-release JAR: the manifest declares `Multi-Release: true`, base classes live at the normal package path, and Java 11-specific classes live under `META-INF/versions/11/`.
3. Compile the base classes for Java 8 compatibility and the Java 11 override classes for Java 11 compatibility.
4. Normalize the JAR so every member has timestamp `2024-01-01T00:00:00Z`.
5. Do not use the network. Do not add extra files to the final JAR.

The policy note in `/home/user/jar_lab/notes/release-policy.txt` is the source of truth for the release layout.
