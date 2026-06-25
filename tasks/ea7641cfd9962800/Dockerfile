FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash coreutils findutils python3 unzip && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p \
      /app/maven-src/classes/com/acme/edgepolicy \
      /app/maven-src/resources/com/acme/edgepolicy \
      /app/repo/com/acme/edge-policy-runtime/2.4.1; \
    printf '%s\n' \
      'compiled fixture for com.acme.edgepolicy.Runtime' \
      'constant-pool: runtime=2.4.1' \
      'abi: linux-neutral' \
      > /app/maven-src/classes/com/acme/edgepolicy/Runtime.class; \
    printf '%s\n' \
      '{"schema":"edge-policy","version":"2026-06","required":["subject","action","resource"]}' \
      > /app/maven-src/resources/com/acme/edgepolicy/schema.json; \
    printf '%s\n' \
      'Edge Policy Runtime' \
      'Copyright 2026 Acme Corp.' \
      'SPDX-License-Identifier: Apache-2.0' \
      > /app/maven-src/LICENSE.txt; \
    printf '%s\n' \
      '<project><modelVersion>4.0.0</modelVersion><groupId>com.acme</groupId><artifactId>edge-policy-runtime</artifactId><version>2.4.1</version><description>stale pom</description></project>' \
      > /app/repo/com/acme/edge-policy-runtime/2.4.1/edge-policy-runtime-2.4.1.pom; \
    printf '%s\n' 'not a jar' \
      > /app/repo/com/acme/edge-policy-runtime/2.4.1/edge-policy-runtime-2.4.1.jar; \
    printf '%s\n' 'stale' \
      > /app/repo/com/acme/edge-policy-runtime/2.4.1/edge-policy-runtime-2.4.1.jar.sha1; \
    printf '%s\n' 'obsolete staging note' \
      > /app/repo/com/acme/edge-policy-runtime/2.4.1/README.tmp; \
    printf '%s\n' '<metadata><stale>true</stale></metadata>' \
      > /app/repo/com/acme/edge-policy-runtime/maven-metadata.xml; \
    printf '%s\n' 'remove this old version' \
      > /app/repo/com/acme/edge-policy-runtime/edge-policy-runtime-2.3.9.jar
