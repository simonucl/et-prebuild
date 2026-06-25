FROM ubuntu:24.04

WORKDIR /home/user/apt_lab

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates coreutils dpkg-dev file gzip python3 \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p /home/user/apt_lab/packages /home/user/apt_lab/build /home/user/apt_lab/repo/dists/bookworm/main/binary-amd64 /home/user/apt_lab/repo/pool/main/stale; \
  \
  mkdir -p /home/user/apt_lab/build/edge-meter/DEBIAN /home/user/apt_lab/build/edge-meter/usr/bin /home/user/apt_lab/build/edge-meter/usr/share/doc/edge-meter; \
  printf '%s\n' \
    'Package: edge-meter' \
    'Version: 1.4.0-1' \
    'Architecture: amd64' \
    'Maintainer: Acme Edge Ops <edge-ops@example.invalid>' \
    'Installed-Size: 28' \
    'Section: net' \
    'Priority: optional' \
    'Homepage: https://example.invalid/acme/edge-meter' \
    'Description: Edge appliance metrics collector' \
    > /home/user/apt_lab/build/edge-meter/DEBIAN/control; \
  printf '#!/bin/sh\nprintf "edge-meter 1.4.0\\n"\n' > /home/user/apt_lab/build/edge-meter/usr/bin/edge-meter; \
  chmod 0755 /home/user/apt_lab/build/edge-meter/usr/bin/edge-meter; \
  printf 'edge-meter offline package\n' > /home/user/apt_lab/build/edge-meter/usr/share/doc/edge-meter/README; \
  \
  mkdir -p /home/user/apt_lab/build/edge-relay/DEBIAN /home/user/apt_lab/build/edge-relay/usr/bin /home/user/apt_lab/build/edge-relay/usr/share/doc/edge-relay; \
  printf '%s\n' \
    'Package: edge-relay' \
    'Version: 0.8.2-2' \
    'Architecture: amd64' \
    'Maintainer: Acme Edge Ops <edge-ops@example.invalid>' \
    'Installed-Size: 36' \
    'Depends: edge-meter (>= 1.4.0), libc6 (>= 2.39)' \
    'Section: net' \
    'Priority: optional' \
    'Homepage: https://example.invalid/acme/edge-relay' \
    'Description: Edge relay control plane shim' \
    > /home/user/apt_lab/build/edge-relay/DEBIAN/control; \
  printf '#!/bin/sh\nprintf "edge-relay 0.8.2\\n"\n' > /home/user/apt_lab/build/edge-relay/usr/bin/edge-relay; \
  chmod 0755 /home/user/apt_lab/build/edge-relay/usr/bin/edge-relay; \
  printf 'edge-relay offline package\n' > /home/user/apt_lab/build/edge-relay/usr/share/doc/edge-relay/README; \
  \
  SOURCE_DATE_EPOCH=1717200000 dpkg-deb --root-owner-group --build /home/user/apt_lab/build/edge-meter /home/user/apt_lab/packages/edge-meter_1.4.0-1_amd64.deb; \
  SOURCE_DATE_EPOCH=1717200000 dpkg-deb --root-owner-group --build /home/user/apt_lab/build/edge-relay /home/user/apt_lab/packages/edge-relay_0.8.2-2_amd64.deb; \
  rm -rf /home/user/apt_lab/build; \
  \
  printf 'stale package index\n' > /home/user/apt_lab/repo/dists/bookworm/main/binary-amd64/Packages; \
  printf 'not gzip\n' > /home/user/apt_lab/repo/dists/bookworm/main/binary-amd64/Packages.gz; \
  printf 'stale release\n' > /home/user/apt_lab/repo/dists/bookworm/Release; \
  printf '{}' > /home/user/apt_lab/repo/manifest.json; \
  printf 'remove me\n' > /home/user/apt_lab/repo/pool/main/stale/old-edge_0.1.0_amd64.deb
