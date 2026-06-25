FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends bash coreutils findutils gzip cpio python3 && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/initramfs-src/{bin,etc/rescue,proc,run,sbin,usr/bin,var/log/rescue,var/tmp}; \
    printf '#!/bin/sh\nset -eu\nmount -t proc proc /proc\nexec /usr/bin/recovery "$@"\n' > /app/initramfs-src/init; \
    printf '#!/bin/sh\necho "recovery shell ready"\n' > /app/initramfs-src/usr/bin/recovery; \
    printf '#!/bin/sh\nprintf "busybox fallback: %s\\n" "$*"\n' > /app/initramfs-src/bin/busybox; \
    printf 'RESCUE_MODE=automatic\nCONSOLE=ttyS0\n' > /app/initramfs-src/etc/rescue/config.env; \
    printf 'do-not-ship\n' > /app/initramfs-src/etc/rescue/local.secret; \
    printf 'boot attempt 17\n' > /app/initramfs-src/var/log/rescue/boot.log; \
    printf 'temporary socket placeholder\n' > /app/initramfs-src/var/tmp/runtime.note; \
    ln -s ../usr/bin/recovery /app/initramfs-src/sbin/recovery; \
    mkfifo /app/initramfs-src/run/recovery.fifo; \
    chmod 0755 /app/initramfs-src/init /app/initramfs-src/usr/bin/recovery /app/initramfs-src/bin/busybox; \
    chmod 0644 /app/initramfs-src/etc/rescue/config.env /app/initramfs-src/etc/rescue/local.secret /app/initramfs-src/var/log/rescue/boot.log /app/initramfs-src/var/tmp/runtime.note; \
    find /app/initramfs-src -exec touch -h -d '2025-03-04 05:06:07 UTC' {} +; \
    mkdir -p /app/handoff; \
    printf 'stale\n' > /app/handoff/rescue-initramfs.cpio.gz; \
    printf '{}\n' > /app/handoff/manifest.json; \
    printf 'stale  rescue-initramfs.cpio.gz\n' > /app/handoff/SHA256SUMS
