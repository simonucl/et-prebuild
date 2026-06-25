FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    cpio \
    findutils \
    gzip \
    python3 \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p \
    /app/rootfs/bin \
    /app/rootfs/etc/rescue \
    /app/rootfs/lib/modules/6.8.0-rescue/kernel/drivers/net \
    /app/rootfs/proc \
    /app/rootfs/sbin \
    /app/rootfs/usr/bin \
    /app/rootfs/var/cache/rescue \
    /app/rootfs/var/lib/rescue; \
  printf '#!/bin/sh\nmount -t proc proc /proc\nexec /usr/bin/rescue-init\n' > /app/rootfs/init; \
  chmod 0755 /app/rootfs/init; \
  printf '#!/bin/sh\necho rescue shell\n' > /app/rootfs/bin/sh; \
  chmod 0755 /app/rootfs/bin/sh; \
  printf '#!/bin/sh\necho starting rescue agent\n' > /app/rootfs/usr/bin/rescue-init; \
  chmod 0755 /app/rootfs/usr/bin/rescue-init; \
  printf 'RESCUE_MODE=offline\nROOT_DEVICE=LABEL=fleet-root\n' > /app/rootfs/etc/rescue/rescue.conf; \
  chmod 0644 /app/rootfs/etc/rescue/rescue.conf; \
  printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOfflineRescueKey operator@fleet\n' > /app/rootfs/etc/rescue/authorized_keys; \
  chmod 0600 /app/rootfs/etc/rescue/authorized_keys; \
  printf 'temporary signing key that must not ship\n' > /app/rootfs/etc/rescue/local.key; \
  chmod 0600 /app/rootfs/etc/rescue/local.key; \
  printf 'rescue-state=clean\nboot-count=0\n' > /app/rootfs/var/lib/rescue/state; \
  chmod 0644 /app/rootfs/var/lib/rescue/state; \
  printf 'cache entry that must not ship\n' > /app/rootfs/var/cache/rescue/blob.cache; \
  printf 'kernel-module-placeholder\n' > /app/rootfs/lib/modules/6.8.0-rescue/kernel/drivers/net/fleetnet.ko; \
  chmod 0644 /app/rootfs/lib/modules/6.8.0-rescue/kernel/drivers/net/fleetnet.ko; \
  ln -s ../usr/bin/rescue-init /app/rootfs/sbin/init; \
  find /app/rootfs -exec touch -h -d '2026-06-25 12:34:56 UTC' {} +
