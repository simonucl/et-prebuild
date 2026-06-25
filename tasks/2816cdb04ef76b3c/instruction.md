# Repair the Ledger Ingest systemd Local Layer

An offline service image is rooted at:

`/home/user/unitroot`

The vendor unit is:

`/home/user/unitroot/usr/lib/systemd/system/ledger-ingest.service`

Do not edit anything under `/home/user/unitroot/usr/lib`. Replace the broken local configuration under `/home/user/unitroot/etc` so the service can be smoke-tested from the image root.

Required end state:

1. The only drop-in for `ledger-ingest.service` must be:

   `/home/user/unitroot/etc/systemd/system/ledger-ingest.service.d/20-offline-hardening.conf`

   It must load `/etc/ledger-ingest/worker.env`, replace the vendor `ExecStart` command with the offline command below, run as the `ledger-ingest` service account, and apply the listed hardening/runtime settings.

   Command:

   `/usr/local/bin/ledger-ingest --config /etc/ledger-ingest/config.yaml --mode ${LEDGER_MODE} --listen ${LEDGER_LISTEN} --spool /var/lib/ledger-ingest/spool --checkpoint /var/lib/ledger-ingest/state/checkpoint.db`

   Settings:

   - `User=ledger-ingest`
   - `Group=ledger-ingest`
   - `SupplementaryGroups=adm`
   - `RuntimeDirectory=ledger-ingest`
   - `RuntimeDirectoryMode=0750`
   - `StateDirectory=ledger-ingest`
   - `StateDirectoryMode=0750`
   - `LogsDirectory=ledger-ingest`
   - `LogsDirectoryMode=0750`
   - `UMask=0027`
   - `NoNewPrivileges=yes`
   - `PrivateTmp=yes`
   - `ProtectSystem=strict`
   - `ProtectHome=yes`
   - `ReadWritePaths=/var/lib/ledger-ingest /var/log/ledger-ingest /run/ledger-ingest`
   - `Restart=on-failure`
   - `RestartSec=5s`

2. Create the environment file:

   `/home/user/unitroot/etc/ledger-ingest/worker.env`

   It must be mode `0600` and contain:

   - `LEDGER_MODE=batch`
   - `LEDGER_LISTEN=127.0.0.1:9191`

3. Create the service config file:

   `/home/user/unitroot/etc/ledger-ingest/config.yaml`

   It must be mode `0640` and describe the spool, checkpoint, log path, and strict replay setting for the offline service.

4. Create a real sysusers policy at:

   `/home/user/unitroot/etc/sysusers.d/ledger-ingest.conf`

   It must define `ledger-ingest` as UID/GID `731`, home `/var/lib/ledger-ingest`, shell `/usr/sbin/nologin`, and add it to the `adm` group.

5. Create a real tmpfiles policy at:

   `/home/user/unitroot/etc/tmpfiles.d/ledger-ingest.conf`

   It must create the service state, spool, and log locations. The state and spool tree must be owned by `ledger-ingest:ledger-ingest`; the log directory must be owned by `ledger-ingest:adm`. Use directory mode `0750` and file mode `0640`. Include an empty checkpoint file at `/var/lib/ledger-ingest/state/checkpoint.db` and an empty current log at `/var/log/ledger-ingest/current.log`.

6. Apply the sysusers and tmpfiles policies once against `/home/user/unitroot` so the current image root already contains the required account entries, directories, and empty files.

7. Write a minified deployment manifest at:

   `/home/user/unitroot/etc/ledger-ingest/deployment-manifest.json`

   It should summarize the repaired local-layer files, final command, service account, managed directories, and hardening settings.

Work offline. Do not use package installation or network access.
