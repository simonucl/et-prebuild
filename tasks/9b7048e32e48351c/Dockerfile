FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash coreutils cpio gzip python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user \
    && mkdir -p /home/user/initramfs_lab/rootfs/{bin,etc,lib/modules/6.8.0-edge,sbin,tmp,var/lib/recovery} \
    && mkdir -p /home/user/initramfs_lab/out \
    && printf '%s\n' '#!/bin/sh' 'export PATH=/bin:/sbin' 'exec /bin/busybox sh' > /home/user/initramfs_lab/rootfs/init \
    && printf '%s\n' '#!/bin/sh' 'echo busybox rescue shell placeholder' > /home/user/initramfs_lab/rootfs/bin/busybox \
    && printf '%s\n' 'mode=rescue' 'root=LABEL=RECOVERY' 'console=ttyS0,115200n8' > /home/user/initramfs_lab/rootfs/etc/recovery.conf \
    && printf '%s\n' 'kernel/drivers/block/loop.ko:' 'kernel/fs/squashfs/squashfs.ko: kernel/lib/decompress_unxz.ko' > /home/user/initramfs_lab/rootfs/lib/modules/6.8.0-edge/modules.dep \
    && printf '%s\n' 'Recovery image payload for the edge appliance.' > /home/user/initramfs_lab/rootfs/var/lib/recovery/README \
    && ln -s ../init /home/user/initramfs_lab/rootfs/sbin/init \
    && printf '%s\n' 'scratch data that must not be archived' > /home/user/initramfs_lab/rootfs/tmp/session.log \
    && printf '%s\n' 'old non-normalized artifact' > /home/user/initramfs_lab/out/recovery-initramfs.cpio.gz \
    && printf '%s\n' '{"status":"stale"}' > /home/user/initramfs_lab/out/recovery-initramfs.manifest.json \
    && chmod 0755 /home/user/initramfs_lab/rootfs/init /home/user/initramfs_lab/rootfs/bin/busybox \
    && chmod 0644 /home/user/initramfs_lab/rootfs/etc/recovery.conf /home/user/initramfs_lab/rootfs/lib/modules/6.8.0-edge/modules.dep /home/user/initramfs_lab/rootfs/var/lib/recovery/README \
    && find /home/user/initramfs_lab/rootfs -exec touch -h -d @1700000000 {} + \
    && chown -R user:user /home/user/initramfs_lab
