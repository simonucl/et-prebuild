FROM debian:trixie-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash rsync jq python3 coreutils diffutils findutils file \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

RUN set -eux; \
    lab=/home/user/rsync-lab; \
    mkdir -p "$lab/baseline/site/assets" "$lab/baseline/site/docs/releases" "$lab/baseline/site/media/v1" "$lab/baseline/site/media/v2" "$lab/baseline/site/tmp" "$lab/baseline/site/bin"; \
    mkdir -p "$lab/desired/site/assets" "$lab/desired/site/docs/releases" "$lab/desired/site/media/v1" "$lab/desired/site/media/v2" "$lab/desired/site/bin"; \
    mkdir -p "$lab/receiver"; \
    printf '<!doctype html>\n<title>Acme Ops Portal</title>\n<link rel="stylesheet" href="assets/app.css">\n<h1>Operations portal</h1>\n<p>Status: staging</p>\n' > "$lab/baseline/site/index.html"; \
    printf 'body { font-family: sans-serif; color: #334; }\n.banner { display: none; }\n' > "$lab/baseline/site/assets/app.css"; \
    printf 'legacy asset\n' > "$lab/baseline/site/assets/old-logo.txt"; \
    printf '# Operator Guide\n\nUse the staging checklist before publishing.\n' > "$lab/baseline/site/docs/guide.md"; \
    printf 'banner v1\n' > "$lab/baseline/site/media/v1/banner.txt"; \
    printf 'banner v2 placeholder\n' > "$lab/baseline/site/media/v2/banner.txt"; \
    ln -s v1/banner.txt "$lab/baseline/site/media/current-banner.txt"; \
    printf 'temporary cache\n' > "$lab/baseline/site/tmp/cache.tmp"; \
    printf '#!/bin/sh\necho old-preview\n' > "$lab/baseline/site/bin/preview"; \
    chmod 0755 "$lab/baseline/site/bin/preview"; \
    printf '<!doctype html>\n<title>Acme Ops Portal</title>\n<link rel="stylesheet" href="assets/app.css">\n<script src="assets/app.js" defer></script>\n<h1>Operations portal</h1>\n<p>Status: production-ready</p>\n' > "$lab/desired/site/index.html"; \
    printf 'body { font-family: system-ui, sans-serif; color: #17202a; }\n.banner { display: block; font-weight: 700; }\n' > "$lab/desired/site/assets/app.css"; \
    printf 'window.portalReady = true;\n' > "$lab/desired/site/assets/app.js"; \
    printf '# Operator Guide\n\nUse the production checklist before publishing.\n' > "$lab/desired/site/docs/guide.md"; \
    printf 'Release 2026-Q3\n- Enable production banner\n- Remove stale cache assets\n' > "$lab/desired/site/docs/releases/2026-q3.md"; \
    printf 'banner v1\n' > "$lab/desired/site/media/v1/banner.txt"; \
    printf 'banner v2 final\n' > "$lab/desired/site/media/v2/banner.txt"; \
    ln -s v2/banner.txt "$lab/desired/site/media/current-banner.txt"; \
    printf '#!/bin/sh\necho production-preview\n' > "$lab/desired/site/bin/preview"; \
    chmod 0755 "$lab/desired/site/bin/preview"; \
    find "$lab/baseline/site" "$lab/desired/site" -exec touch -h -d '2026-06-25 00:00:00 UTC' {} +; \
    rsync -a --delete "$lab/baseline/site/" "$lab/receiver/site/"; \
    printf 'stale batch\n' > "$lab/handoff.tmp"; \
    chown -R user:user "$lab"

USER user
