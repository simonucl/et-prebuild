FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      bash \
      coreutils \
      findutils \
      gzip \
      python3 \
      tar && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m user || true

RUN set -eux; \
    mkdir -p /home/user/oci-stage/rootfs/etc/acme-cache \
             /home/user/oci-stage/rootfs/usr/local/bin \
             /home/user/oci-stage/rootfs/var/lib/acme-cache \
             /home/user/oci-stage/rootfs/tmp \
             /home/user/oci-stage/rootfs/tests \
             /home/user/oci-stage/notes \
             /home/user/oci-export; \
    printf 'listen: 127.0.0.1:9184\nmode: strict\ncache_ttl: 3600\n' > /home/user/oci-stage/rootfs/etc/acme-cache/config.yaml; \
    printf '#!/usr/bin/env bash\nset -euo pipefail\nprintf "acme-cache 1.2.0\\n"\n' > /home/user/oci-stage/rootfs/usr/local/bin/acme-cache; \
    printf 'seed=offline\nwindow=2024q4\n' > /home/user/oci-stage/rootfs/var/lib/acme-cache/seed.txt; \
    ln -s config.yaml /home/user/oci-stage/rootfs/etc/acme-cache/current; \
    printf 'temporary runtime file that must not be shipped\n' > /home/user/oci-stage/rootfs/tmp/session.tmp; \
    printf 'source-only fixture that must not be shipped\n' > /home/user/oci-stage/rootfs/tests/fixture.txt; \
    printf 'do not place this note in the OCI layout\n' > /home/user/oci-stage/notes/operator.md; \
    printf '{"created":"2024-02-03T04:05:06Z","architecture":"amd64","os":"linux","tag":"acme-cache:1.2.0"}\n' > /home/user/oci-stage/image-meta.json; \
    chmod 0755 /home/user/oci-stage/rootfs/usr/local/bin/acme-cache; \
    chmod 0644 /home/user/oci-stage/rootfs/etc/acme-cache/config.yaml \
               /home/user/oci-stage/rootfs/var/lib/acme-cache/seed.txt \
               /home/user/oci-stage/rootfs/tmp/session.tmp \
               /home/user/oci-stage/rootfs/tests/fixture.txt \
               /home/user/oci-stage/image-meta.json \
               /home/user/oci-stage/notes/operator.md; \
    find /home/user/oci-stage -type d -exec chmod 0755 {} +; \
    touch -h -d '2025-06-02 10:12:00 UTC' /home/user/oci-stage/rootfs/etc/acme-cache/config.yaml; \
    touch -h -d '2024-12-11 07:00:03 UTC' /home/user/oci-stage/rootfs/usr/local/bin/acme-cache; \
    touch -h -d '2023-09-14 01:02:03 UTC' /home/user/oci-stage/rootfs/var/lib/acme-cache/seed.txt; \
    touch -h -d '2025-01-01 00:00:00 UTC' /home/user/oci-stage/rootfs/etc/acme-cache/current; \
    chown -R user:user /home/user/oci-stage /home/user/oci-export

CMD ["bash"]
