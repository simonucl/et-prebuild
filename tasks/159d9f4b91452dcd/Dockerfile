FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y \
    apt-utils \
    bash \
    dpkg-dev \
    gzip \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN set -eux; \
    mkdir -p /tmp/edge-agent-pkg/DEBIAN \
      /tmp/edge-agent-pkg/usr/bin \
      /tmp/edge-agent-pkg/usr/share/doc/edge-agent \
      /home/user/aptrepo/pool/main/e/edge-agent \
      /home/user/aptrepo/dists/stable/main/binary-amd64 \
      /home/user/apt-client \
      /opt/aptrepo-expected; \
    printf '%s\n' \
      'Package: edge-agent' \
      'Version: 1.2.3' \
      'Architecture: all' \
      'Maintainer: Edge Ops <edge@example.invalid>' \
      'Priority: optional' \
      'Section: admin' \
      'Description: Edge telemetry bootstrap agent' \
      ' A tiny internal package used to test offline APT handoffs.' \
      > /tmp/edge-agent-pkg/DEBIAN/control; \
    printf '%s\n' '#!/bin/sh' 'echo edge-agent 1.2.3' > /tmp/edge-agent-pkg/usr/bin/edge-agent; \
    chmod 0755 /tmp/edge-agent-pkg/usr/bin/edge-agent; \
    printf '%s\n' 'edge-agent offline package fixture' > /tmp/edge-agent-pkg/usr/share/doc/edge-agent/README; \
    find /tmp/edge-agent-pkg -exec touch -h -d '2024-01-01 00:00:00 UTC' {} +; \
    dpkg-deb --root-owner-group -Zgzip --build /tmp/edge-agent-pkg /home/user/aptrepo/pool/main/e/edge-agent/edge-agent_1.2.3_all.deb; \
    sha256sum /home/user/aptrepo/pool/main/e/edge-agent/edge-agent_1.2.3_all.deb > /opt/aptrepo-expected/edge-agent_1.2.3_all.deb.sha256; \
    printf '%s\n' \
      'Package: edge-agent' \
      'Architecture: all' \
      'Version: 1.2.2' \
      'Filename: pool/main/e/edge-agent/edge-agent_1.2.2_all.deb' \
      'Size: 12' \
      'MD5sum: 00000000000000000000000000000000' \
      'SHA1: 0000000000000000000000000000000000000000' \
      'SHA256: 0000000000000000000000000000000000000000000000000000000000000000' \
      'Description: stale index entry' \
      > /home/user/aptrepo/dists/stable/main/binary-amd64/Packages; \
    gzip -c /home/user/aptrepo/dists/stable/main/binary-amd64/Packages > /home/user/aptrepo/dists/stable/main/binary-amd64/Packages.gz; \
    printf '%s\n' \
      'Origin: stale' \
      'Label: stale' \
      'Suite: oldstable' \
      'Codename: oldstable' \
      'Architectures: i386' \
      'Components: contrib' \
      > /home/user/aptrepo/dists/stable/Release; \
    printf '%s\n' 'deb http://invalid.example.invalid/debian stable main' > /home/user/apt-client/sources.list; \
    chown -R user:user /home/user/aptrepo /home/user/apt-client
