FROM ghcr.io/simonucl/et-envs:2336009141deb9ac

WORKDIR /app

RUN id -u user >/dev/null 2>&1 || useradd -m -s /bin/bash user

RUN set -eux; \
    rm -rf /home/user/unitroot; \
    mkdir -p /home/user/unitroot/etc; \
    printf 'root:x:0:0:root:/root:/bin/bash\n' > /home/user/unitroot/etc/passwd; \
    printf 'root:x:0:\nadm:x:4:\n' > /home/user/unitroot/etc/group; \
    mkdir -p /home/user/unitroot/usr/lib/sysusers.d \
             /home/user/unitroot/usr/lib/tmpfiles.d \
             /home/user/unitroot/etc/sysusers.d \
             /home/user/unitroot/etc/tmpfiles.d \
             /home/user/unitroot/usr/share/edge-collector/defaults \
             /home/user/unitroot/var/cache/edge-collector; \
    printf 'u edgeold 480 \"obsolete edge user\" /nonexistent -\n' > /home/user/unitroot/usr/lib/sysusers.d/edge-collector.conf; \
    printf 'd /var/lib/edge-collector 0777 root root -\n' > /home/user/unitroot/usr/lib/tmpfiles.d/edge-collector.conf; \
    printf '{\"version\":1,\"flush_interval\":\"60s\",\"inputs\":[\"stale\"]}\n' > /home/user/unitroot/usr/share/edge-collector/defaults/config.json; \
    printf 'orphan-cache\n' > /home/user/unitroot/var/cache/edge-collector/stale.tmp; \
    find /home/user/unitroot -type d -exec chmod 0755 {} +

WORKDIR /home/user
