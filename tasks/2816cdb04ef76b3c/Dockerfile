FROM ghcr.io/simonucl/et-envs:2336009141deb9ac

WORKDIR /app

RUN id -u user >/dev/null 2>&1 || useradd -m -s /bin/bash user

RUN rm -rf /home/user/unitroot \
  && mkdir -p \
    /home/user/unitroot/usr/lib/systemd/system \
    /home/user/unitroot/etc/systemd/system/ledger-ingest.service.d \
    /home/user/unitroot/etc/ledger-ingest \
    /home/user/unitroot/etc/tmpfiles.d \
    /home/user/unitroot/etc/sysusers.d \
    /home/user/unitroot/etc/default \
    /home/user/unitroot/var/lib/ledger-ingest \
    /home/user/unitroot/var/log \
    /home/user/unitroot/usr/local/bin \
  && printf 'root:x:0:0:root:/root:/bin/bash\n' > /home/user/unitroot/etc/passwd \
  && printf 'root:x:0:\nadm:x:4:\n' > /home/user/unitroot/etc/group \
  && printf 'shadow:x:42:\n' > /home/user/unitroot/etc/gshadow \
  && touch /home/user/unitroot/etc/shadow \
  && printf '#!/bin/sh\nexec sleep infinity\n' > /home/user/unitroot/usr/local/bin/ledger-ingest \
  && chmod 0755 /home/user/unitroot/usr/local/bin/ledger-ingest \
  && printf '%s\n' \
    '[Unit]' \
    'Description=Ledger ingest worker' \
    'After=network-online.target' \
    'Wants=network-online.target' \
    '' \
    '[Service]' \
    'Type=simple' \
    'EnvironmentFile=-/etc/default/ledger-ingest' \
    'ExecStart=/usr/local/bin/ledger-ingest --config /etc/default/legacy.yaml --mode stream --listen 0.0.0.0:8080' \
    'Restart=always' \
    '' \
    '[Install]' \
    'WantedBy=multi-user.target' \
    > /home/user/unitroot/usr/lib/systemd/system/ledger-ingest.service \
  && printf '%s\n' \
    '[Service]' \
    'Environment=LEDGER_MODE=stream' \
    'ProtectSystem=no' \
    'ReadWritePaths=/tmp' \
    > /home/user/unitroot/etc/systemd/system/ledger-ingest.service.d/10-stale-local.conf \
  && printf '%s\n' \
    'LEDGER_CONFIG=/etc/default/legacy.yaml' \
    'LEDGER_MODE=stream' \
    'LEDGER_LISTEN=0.0.0.0:8080' \
    > /home/user/unitroot/etc/default/ledger-ingest \
  && printf '%s\n' \
    'd /var/lib/ledger-ingest 0777 root root -' \
    'd /var/log/ledger-ingest 0777 root root -' \
    > /home/user/unitroot/etc/tmpfiles.d/ledger-ingest.conf \
  && printf '%s\n' \
    'u ledger-ingest 999 "temporary debug service" /tmp /bin/sh' \
    > /home/user/unitroot/etc/sysusers.d/ledger-ingest.conf \
  && printf '{"service":"ledger-ingest","status":"stale"}\n' > /home/user/unitroot/etc/ledger-ingest/deployment-manifest.json \
  && chown -R user:user /home/user/unitroot
