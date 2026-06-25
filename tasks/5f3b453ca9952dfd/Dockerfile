FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates coreutils findutils python3 unzip zip \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p \
      /app/staging/classes/com/acme/telemetry/internal \
      /app/staging/resources/META-INF/services \
      /app/staging/sources/com/acme/telemetry/internal \
      /app/repo/com/acme/telemetry-agent/2.4.1; \
    printf 'compiled-bytecode:Agent:v2.4.1\nrequires=Config\n' > /app/staging/classes/com/acme/telemetry/Agent.class; \
    printf 'compiled-bytecode:Config:v2.4.1\nmode=offline\n' > /app/staging/classes/com/acme/telemetry/internal/Config.class; \
    printf 'com.acme.telemetry.internal.Config\n' > /app/staging/resources/META-INF/services/com.acme.telemetry.Plugin; \
    printf '%s\n' \
      'package com.acme.telemetry;' \
      '' \
      'public final class Agent {' \
      '  public static String id() {' \
      '    return "telemetry-agent-2.4.1";' \
      '  }' \
      '}' \
      > /app/staging/sources/com/acme/telemetry/Agent.java; \
    printf '%s\n' \
      'package com.acme.telemetry.internal;' \
      '' \
      'public final class Config {' \
      '  public static String mode() {' \
      '    return "offline";' \
      '  }' \
      '}' \
      > /app/staging/sources/com/acme/telemetry/internal/Config.java; \
    printf '%s\n' 'Telemetry Agent Fixture' 'SPDX-License-Identifier: Apache-2.0' > /app/staging/LICENSE.txt; \
    printf '%s\n' \
      '<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">' \
      '  <modelVersion>4.0.0</modelVersion>' \
      '  <groupId>com.acme</groupId>' \
      '  <artifactId>telemetry-agent</artifactId>' \
      '  <version>2.4.1</version>' \
      '  <packaging>jar</packaging>' \
      '  <name>Telemetry Agent</name>' \
      '</project>' \
      > /app/staging/pom.xml; \
    printf 'stale jar\n' > /app/repo/com/acme/telemetry-agent/2.4.1/telemetry-agent-2.4.1.jar; \
    printf 'stale sources\n' > /app/repo/com/acme/telemetry-agent/2.4.1/telemetry-agent-2.4.1-sources.jar; \
    printf '<project>broken</project>\n' > /app/repo/com/acme/telemetry-agent/2.4.1/telemetry-agent-2.4.1.pom; \
    printf '<metadata><broken>true</broken></metadata>\n' > /app/repo/com/acme/telemetry-agent/maven-metadata.xml; \
    find /app/staging /app/repo -exec touch -h -d '2026-06-24 12:34:56 UTC' {} +
