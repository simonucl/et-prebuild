FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    acl \
    attr \
    bash \
    coreutils \
    findutils \
    gzip \
    python3 \
    tar \
  && rm -rf /var/lib/apt/lists/*

RUN if ! id -u user >/dev/null 2>&1; then useradd -m -u 2000 user; fi \
  && if ! id -u backup >/dev/null 2>&1; then useradd -M -u 2300 -s /usr/sbin/nologin backup || useradd -M -s /usr/sbin/nologin backup; fi \
  && mkdir -p \
    /home/user/evidence/rootfs/etc/edge \
    /home/user/evidence/rootfs/usr/local/bin \
    /home/user/evidence/rootfs/var/lib/edge \
    /home/user/evidence/rootfs/share/releases/2026.06.25 \
    /home/user/evidence/handoff \
  && printf 'policy_version=7\nmode=offline\nallow_debug=false\n' > /home/user/evidence/rootfs/etc/edge/policy.conf \
  && printf '#!/bin/sh\nset -eu\nprintf "edge ok\\n"\n' > /home/user/evidence/rootfs/usr/local/bin/edge-health \
  && chmod 0755 /home/user/evidence/rootfs/usr/local/bin/edge-health \
  && ln /home/user/evidence/rootfs/usr/local/bin/edge-health /home/user/evidence/rootfs/usr/local/bin/edge-health-current \
  && printf 'release=2026.06.25\nchannel=stable\n' > /home/user/evidence/rootfs/share/releases/2026.06.25/manifest.txt \
  && ln -s releases/2026.06.25 /home/user/evidence/rootfs/share/current \
  && truncate -s 1048576 /home/user/evidence/rootfs/var/lib/edge/cache.db \
  && printf 'EDGEIDX' | dd of=/home/user/evidence/rootfs/var/lib/edge/cache.db bs=1 seek=4096 conv=notrunc status=none \
  && setfattr -n user.release.channel -v stable /home/user/evidence/rootfs/etc/edge/policy.conf \
  && setfacl -m u:backup:r-- /home/user/evidence/rootfs/var/lib/edge/cache.db \
  && printf 'stale\n' > /home/user/evidence/handoff/edge-root.pax.tar.gz \
  && printf '{"stale":true}\n' > /home/user/evidence/handoff/manifest.json \
  && printf 'old checksum\n' > /home/user/evidence/handoff/SHA256SUMS \
  && chown -R user:user /home/user/evidence \
  && chown backup:backup /home/user/evidence/rootfs/var/lib/edge/cache.db \
  && setfacl -m u:backup:r-- /home/user/evidence/rootfs/var/lib/edge/cache.db
