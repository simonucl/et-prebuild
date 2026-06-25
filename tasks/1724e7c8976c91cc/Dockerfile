FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash coreutils findutils gzip tar python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

WORKDIR /home/user/lfs_capsule

RUN set -eux; \
    mkdir -p source/assets source/src handoff worktree objects; \
    python3 -c 'from pathlib import Path; root=Path("/home/user/lfs_capsule"); (root/"source/README.md").write_text("# Edge Telemetry Filters\n\nThis package ships the offline calibration data used by the edge telemetry\nfilter. Binary payloads must be handed off through the internal LFS capsule.\n", encoding="utf-8"); (root/"source/src/filter.py").write_text("from pathlib import Path\n\n\ndef payload_names(root: Path) -> list[str]:\n    return sorted(p.name for p in (root / \"assets\").glob(\"*.bin\"))\n", encoding="utf-8"); assets=root/"source/assets"; sensor=bytes((i*37+11)%256 for i in range(4096)); model=b"EDGEMODEL-v2\\0"+bytes((255-(i*19%256)) for i in range(6144)); (assets/"sensor-calibration.bin").write_bytes(sensor); (assets/"field-model.bin").write_bytes(model)'; \
    find /home/user/lfs_capsule -type d -exec chmod 0755 {} +; \
    find /home/user/lfs_capsule -type f -exec chmod 0644 {} +; \
    chown -R user:user /home/user/lfs_capsule

USER user
