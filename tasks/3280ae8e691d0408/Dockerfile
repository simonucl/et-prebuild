FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash coreutils findutils python3 unzip zip openjdk-17-jdk-headless && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p \
      /app/staging/classes/com/acme/telemetry/internal \
      /app/staging/classes/META-INF/services \
      /app/maven-repo/com/acme/telemetry-core/2.7.1 \
      /app/maven-repo/com/acme/telemetry-core; \
    printf '%s\n' \
      '<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">' \
      '  <modelVersion>4.0.0</modelVersion>' \
      '  <groupId>com.acme</groupId>' \
      '  <artifactId>telemetry-core</artifactId>' \
      '  <version>2.7.1</version>' \
      '  <packaging>jar</packaging>' \
      '  <name>Acme Telemetry Core</name>' \
      '  <description>Offline fixture for deterministic Maven repository publishing.</description>' \
      '</project>' \
      > /app/staging/pom.xml; \
    printf '%s\n' \
      'compiled-bytecode: Collector' \
      'major=61' \
      'sha-source=collector-v2' \
      > /app/staging/classes/com/acme/telemetry/Collector.class; \
    printf '%s\n' \
      'compiled-bytecode: Envelope' \
      'major=61' \
      'sha-source=envelope-v4' \
      > /app/staging/classes/com/acme/telemetry/internal/Envelope.class; \
    printf '%s\n' 'com.acme.telemetry.Collector' \
      > /app/staging/classes/META-INF/services/com.acme.telemetry.Plugin; \
    printf '%s\n' 'stale jar bytes' \
      > /app/maven-repo/com/acme/telemetry-core/2.7.1/telemetry-core-2.7.1.jar; \
    printf '%s\n' '<project>broken</project>' \
      > /app/maven-repo/com/acme/telemetry-core/2.7.1/telemetry-core-2.7.1.pom; \
    printf '%s\n' '<metadata><broken>true</broken></metadata>' \
      > /app/maven-repo/com/acme/telemetry-core/maven-metadata.xml
