FROM ubuntu:24.04

WORKDIR /home/user/repo_lab

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash dpkg-dev gzip python3 apt \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    useradd -m -s /bin/bash user; \
    mkdir -p /home/user/repo_lab/pool/main/a/acme-metrics-agent \
             /home/user/repo_lab/pool/main/a/acme-metrics-tools \
             /home/user/repo_lab/dists/stable/main/binary-amd64; \
    build_pkg() { \
      name="$1"; version="$2"; arch="$3"; script_name="$4"; script_body="$5"; out_dir="$6"; \
      root="/tmp/pkg-${name}-${version}-${arch}"; \
      rm -rf "$root"; \
      mkdir -p "$root/DEBIAN" "$root/usr/bin" "$root/usr/share/doc/$name"; \
      printf 'Package: %s\nVersion: %s\nSection: utils\nPriority: optional\nArchitecture: %s\nMaintainer: Acme Ops <ops@example.com>\nDescription: Offline Acme metrics package %s\n' "$name" "$version" "$arch" "$name" > "$root/DEBIAN/control"; \
      printf '#!/bin/sh\n%s\n' "$script_body" > "$root/usr/bin/$script_name"; \
      chmod 0755 "$root/usr/bin/$script_name"; \
      printf '%s %s\n' "$name" "$version" > "$root/usr/share/doc/$name/README"; \
      dpkg-deb --root-owner-group --build "$root" "$out_dir/${name}_${version}_${arch}.deb"; \
      rm -rf "$root"; \
    }; \
    build_pkg acme-metrics-agent 1.4.0 amd64 acme-agent-report 'echo acme-agent 1.4.0 stale' /home/user/repo_lab/pool/main/a/acme-metrics-agent; \
    build_pkg acme-metrics-agent 1.4.1 amd64 acme-agent-report 'echo acme-agent 1.4.1 ready' /home/user/repo_lab/pool/main/a/acme-metrics-agent; \
    build_pkg acme-metrics-tools 0.9.0 all acme-metrics-summarize 'printf "acme-metrics-tools 0.9.0\\n"' /home/user/repo_lab/pool/main/a/acme-metrics-tools; \
    cd /home/user/repo_lab; \
    dpkg-scanpackages --arch amd64 pool /dev/null > /tmp/Packages.current; \
    awk 'BEGIN{RS=""; ORS="\\n\\n"} /Package: acme-metrics-agent/ && /Version: 1.4.0/' /tmp/Packages.current > dists/stable/main/binary-amd64/Packages; \
    gzip -c dists/stable/main/binary-amd64/Packages > dists/stable/main/binary-amd64/Packages.gz; \
    printf '%s\n' \
      'Archive: stable' \
      'Codename: stale' \
      'Suite: stable' \
      'Component: main' \
      'Origin: Old Mirror' \
      'Label: Old Mirror' \
      'Architectures: amd64' \
      'Date: Mon, 01 Jan 2024 00:00:00 +0000' \
      > dists/stable/Release
RUN set -eux; \
    printf '%s\n' '{"suite":"stable","component":"main","architecture":"amd64","packages":[{"name":"acme-metrics-agent","version":"1.4.0","filename":"pool/main/a/acme-metrics-agent/acme-metrics-agent_1.4.0_amd64.deb","sha256":"stale"}]}' > /home/user/repo_lab/manifest.json
RUN chown -R user:user /home/user/repo_lab
