FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates openjdk-21-jdk-headless python3 zip unzip coreutils findutils \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

WORKDIR /home/user

RUN mkdir -p /home/user/jar_lab/src/com/acme/scrub/rules /home/user/jar_lab/src/META-INF/services /home/user/jar_lab/dist

RUN printf '%s\n' \
    'package com.acme.scrub;' \
    '' \
    'public interface Scrubber {' \
    '    String scrub(String input);' \
    '}' \
    > /home/user/jar_lab/src/com/acme/scrub/Scrubber.java

RUN printf '%s\n' \
    'package com.acme.scrub;' \
    '' \
    'import java.util.regex.Pattern;' \
    '' \
    'public final class Redactor implements Scrubber {' \
    '    private static final Pattern EMAIL = Pattern.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,}");' \
    '    private static final Pattern TOKEN = Pattern.compile("(?i)(api[_-]?key|token)=([A-Za-z0-9._-]{6,})");' \
    '' \
    '    @Override' \
    '    public String scrub(String input) {' \
    '        String noEmail = EMAIL.matcher(input).replaceAll("[redacted-email]");' \
    '        return TOKEN.matcher(noEmail).replaceAll("$1=[redacted-secret]");' \
    '    }' \
    '}' \
    > /home/user/jar_lab/src/com/acme/scrub/Redactor.java

RUN printf '%s\n' \
    'package com.acme.scrub;' \
    '' \
    'import java.io.BufferedReader;' \
    'import java.io.InputStreamReader;' \
    'import java.nio.charset.StandardCharsets;' \
    '' \
    'public final class Main {' \
    '    public static void main(String[] args) throws Exception {' \
    '        Scrubber scrubber = new Redactor();' \
    '        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8))) {' \
    '            String line;' \
    '            while ((line = reader.readLine()) != null) {' \
    '                System.out.println(scrubber.scrub(line));' \
    '            }' \
    '        }' \
    '    }' \
    '}' \
    > /home/user/jar_lab/src/com/acme/scrub/Main.java

RUN printf '%s\n' \
    '# default scrubber rule metadata' \
    'email=[redacted-email]' \
    'secret=[redacted-secret]' \
    > /home/user/jar_lab/src/com/acme/scrub/rules/default-rules.txt

RUN printf '%s\n' 'com.acme.scrub.Redactor' > /home/user/jar_lab/src/META-INF/services/com.acme.scrub.Scrubber

RUN printf 'stale artifact\n' > /home/user/jar_lab/dist/log-scrubber-1.2.0.jar \
    && printf 'old checksum\n' > /home/user/jar_lab/dist/SHA256SUMS \
    && printf 'remove me\n' > /home/user/jar_lab/dist/debug.tmp

RUN chown -R user:user /home/user/jar_lab

USER user
WORKDIR /home/user
