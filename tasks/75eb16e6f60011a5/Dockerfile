FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    coreutils \
    cpio \
    gzip \
    python3 \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

RUN set -eux; \
  mkdir -p /home/user/initramfs_lab/source/bin /home/user/initramfs_lab/source/etc /home/user/initramfs_lab/source/sbin /home/user/initramfs_lab/out; \
  printf '#!/bin/sh\nset -eu\nmount -t proc proc /proc 2>/dev/null || true\nexec /bin/sh\n' > /home/user/initramfs_lab/source/init; \
  printf '#!/bin/sh\nprintf "busybox rescue shell\\n"\n' > /home/user/initramfs_lab/source/bin/busybox; \
  printf 'ACME edge rescue initramfs\n' > /home/user/initramfs_lab/source/etc/issue; \
  printf 'ttyS0::respawn:/bin/sh\n' > /home/user/initramfs_lab/source/etc/mdev.conf; \
  ln -s busybox /home/user/initramfs_lab/source/bin/sh; \
  ln -s ../init /home/user/initramfs_lab/source/sbin/init; \
  chmod 0755 /home/user/initramfs_lab/source/init /home/user/initramfs_lab/source/bin/busybox; \
  chmod 0644 /home/user/initramfs_lab/source/etc/issue /home/user/initramfs_lab/source/etc/mdev.conf; \
  find /home/user/initramfs_lab/source -exec touch -h -d '2024-05-01 12:00:00 UTC' {} +; \
  printf 'stale\n' > /home/user/initramfs_lab/out/rescue-initramfs.cpio.gz; \
  printf '{}\n' > /home/user/initramfs_lab/out/manifest.json; \
  printf 'stale  rescue-initramfs.cpio.gz\n' > /home/user/initramfs_lab/out/SHA256SUMS; \
  chown -R user:user /home/user/initramfs_lab

USER user
