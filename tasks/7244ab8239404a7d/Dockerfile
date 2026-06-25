FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && apt-get install -y \
    apt-utils \
    dpkg-dev \
    gnupg \
    gzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/incoming /app/repo /app/signing/gnupg; \
    chmod 700 /app/signing/gnupg; \
    make_deb() { \
      pkg="$1"; ver="$2"; arch="$3"; desc="$4"; bin="$5"; \
      work="/tmp/pkg-${pkg}-${ver}-${arch}"; \
      mkdir -p "$work/DEBIAN" "$work/usr/bin" "$work/usr/share/doc/$pkg"; \
      printf 'Package: %s\nVersion: %s\nSection: admin\nPriority: optional\nArchitecture: %s\nMaintainer: Acme Release <release@acme.invalid>\nDescription: %s\n' "$pkg" "$ver" "$arch" "$desc" > "$work/DEBIAN/control"; \
      printf '#!/bin/sh\nprintf "%s %s\\n"\n' "$pkg" "$ver" > "$work/usr/bin/$bin"; \
      chmod 0755 "$work/usr/bin/$bin"; \
      printf '%s %s offline fixture\n' "$pkg" "$ver" > "$work/usr/share/doc/$pkg/README"; \
      dpkg-deb --root-owner-group --build "$work" "/app/incoming/${pkg}_${ver}_${arch}.deb"; \
      rm -rf "$work"; \
    }; \
    make_deb edge-agent 1.4.0 amd64 "Edge agent previous stable build" edge-agent; \
    make_deb edge-agent 1.4.1 amd64 "Edge agent current hotfix build" edge-agent; \
    make_deb relayctl 0.9.2 amd64 "Relay control helper" relayctl; \
    printf '%s\n' \
      'Key-Type: RSA' \
      'Key-Length: 2048' \
      'Name-Real: Acme Offline Repo' \
      'Name-Email: repo@acme.invalid' \
      'Expire-Date: 0' \
      '%no-protection' \
      '%commit' > /tmp/key.batch; \
    GNUPGHOME=/app/signing/gnupg gpg --batch --generate-key /tmp/key.batch; \
    GNUPGHOME=/app/signing/gnupg gpg --armor --export 'repo@acme.invalid' > /app/signing/acme-offline-repo.asc; \
    chmod -R go-rwx /app/signing/gnupg; \
    rm -f /tmp/key.batch
