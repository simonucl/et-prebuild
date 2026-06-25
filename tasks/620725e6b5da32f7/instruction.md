# Repair the edge-collector offline install profile

An interrupted package migration left an offline root tree at:

`/home/user/unitroot`

Do not modify or delete the packaged defaults under `/home/user/unitroot/usr/lib`. Install local administrator overrides under `/home/user/unitroot/etc` and apply them to the offline root.

Your final state must satisfy all of the following:

1. Create `/home/user/unitroot/etc/sysusers.d/edge-collector.conf`.
   - It must define a system group `edge-collector` with GID `472`.
   - It must define a system user `edge-collector` with UID `472`, primary group `edge-collector`, description `Edge Collector`, home directory `/var/lib/edge-collector`, and shell `/usr/sbin/nologin`.
   - It must add `edge-collector` to the supplementary group `adm`.

2. Apply the sysusers configuration to `/home/user/unitroot` so the offline root contains the matching entries in its account databases.

3. Create `/home/user/unitroot/etc/tmpfiles.d/edge-collector.conf`.
   - `/var/lib/edge-collector` must be a directory owned by `edge-collector:edge-collector` with mode `0750`.
   - `/var/lib/edge-collector/spool`, `/var/lib/edge-collector/state`, and `/var/log/edge-collector` must be directories owned by `edge-collector:adm` with mode `0750`.
   - `/var/lib/edge-collector/config.json` must be created from `/usr/share/edge-collector/defaults/config.json`, owned by `edge-collector:edge-collector`, with mode `0640`.
   - `/var/lib/edge-collector/state/checkpoint.json` must be a regular file owned by `edge-collector:edge-collector`, with mode `0640`.
   - `/var/cache/edge-collector` and its stale contents must be removed recursively.

4. Apply the tmpfiles configuration to `/home/user/unitroot`.

5. Replace `/home/user/unitroot/var/lib/edge-collector/state/checkpoint.json` with exactly this JSON, minified on one line with a trailing newline:

   ```json
   {"cursor":"2024-05-14T10:15:00Z","offset":0,"clean_shutdown":true}
   ```

6. Create `/home/user/unitroot/etc/edge-collector/install-manifest.json` as minified JSON on one line with one trailing newline. Its top-level keys must appear in this order:

   ```json
   {
     "sysusers": "/etc/sysusers.d/edge-collector.conf",
     "tmpfiles": "/etc/tmpfiles.d/edge-collector.conf",
     "user": "edge-collector",
     "uid": 472,
     "gid": 472,
     "managed_paths": [
       "/var/lib/edge-collector",
       "/var/lib/edge-collector/spool",
       "/var/lib/edge-collector/state",
       "/var/lib/edge-collector/config.json",
       "/var/lib/edge-collector/state/checkpoint.json",
       "/var/log/edge-collector"
     ],
     "cache_removed": true
   }
   ```

Use the real `systemd-sysusers` and `systemd-tmpfiles` tools when applying the configuration. The host system outside `/home/user/unitroot` must not be changed.
