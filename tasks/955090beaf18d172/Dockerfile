FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash coreutils findutils gzip python3 tar \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p /home/user/oci-dual/basefs/etc/netprobe \
           /home/user/oci-dual/basefs/usr/local/bin \
           /home/user/oci-dual/basefs/usr/share/netprobe \
           /home/user/oci-dual/basefs/var/lib/netprobe/cache \
           /home/user/oci-dual/patchfs/etc/netprobe \
           /home/user/oci-dual/patchfs/usr/local/bin \
           /home/user/oci-dual/patchfs/var/lib/netprobe/cache \
           /home/user/oci-dual/image/blobs/sha256; \
  printf 'listen: 127.0.0.1:9000\nmode: lab\nsample_rate: 10\n' > /home/user/oci-dual/basefs/etc/netprobe/defaults.yaml; \
  printf '#!/bin/sh\nset -eu\nprintf "netprobe base\\n"\n' > /home/user/oci-dual/basefs/usr/local/bin/netprobe; \
  chmod 0755 /home/user/oci-dual/basefs/usr/local/bin/netprobe; \
  printf '{"type":"object","required":["listen","mode","sample_rate"]}\n' > /home/user/oci-dual/basefs/usr/share/netprobe/schema.json; \
  printf 'checkpoint=17\n' > /home/user/oci-dual/basefs/var/lib/netprobe/cache/state.txt; \
  printf 'listen: 0.0.0.0:9443\nmode: offline\nsample_rate: 3\nsink: file\n' > /home/user/oci-dual/patchfs/etc/netprobe/config.yaml; \
  chmod 0640 /home/user/oci-dual/patchfs/etc/netprobe/config.yaml; \
  printf '#!/bin/sh\nset -eu\nprintf "netprobe offline 2.1.0\\n"\n' > /home/user/oci-dual/patchfs/usr/local/bin/netprobe; \
  chmod 0755 /home/user/oci-dual/patchfs/usr/local/bin/netprobe; \
  printf 'checkpoint=0\n' > /home/user/oci-dual/patchfs/var/lib/netprobe/cache/state.txt; \
  printf 'stale\n' > /home/user/oci-dual/image/index.json; \
  printf '{}' > /home/user/oci-dual/image/oci-layout; \
  printf 'do not keep this blob\n' > /home/user/oci-dual/image/blobs/sha256/stale; \
  find /home/user/oci-dual -type d -exec chmod 0755 {} +
