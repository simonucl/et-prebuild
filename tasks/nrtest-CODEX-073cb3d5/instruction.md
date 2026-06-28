# Repair the SSH Client Profile

An automation host has a broken OpenSSH client profile under `/home/user/.ssh`.
Your job is to repair it so that later deployment scripts can query the effective
client settings with `ssh -G` and get the intended values without opening any
network connection.

Important OpenSSH behavior to account for: client configuration is read from top
to bottom, and for each parameter the first obtained value is used. Broad `Host`
blocks must therefore not shadow more specific host blocks.

Required final state:

1. `/home/user/.ssh/config` must include all files matching
   `/home/user/.ssh/conf.d/*.conf` and must provide these fallback values for
   `Host *`:
   - `ServerAliveInterval 30`
   - `TCPKeepAlive no`
   - `IdentitiesOnly yes`

2. The effective `ssh -G -F /home/user/.ssh/config <alias>` settings must match:

   | alias | hostname | user | port | proxyjump | identityfile | stricthostkeychecking |
   | --- | --- | --- | --- | --- | --- | --- |
   | `prod-bastion` | `bastion.prod.internal` | `ops` | `2222` | none | `~/.ssh/keys/prod_ed25519` | `true` |
   | `prod-db` | `db01.prod.internal` | `postgres` | `2222` | `prod-bastion` | `~/.ssh/keys/prod_ed25519` | `true` |
   | `staging-bastion` | `bastion.staging.internal` | `ops` | `2201` | none | `~/.ssh/keys/staging_ed25519` | `accept-new` |
   | `staging-api` | `api.staging.internal` | `deploy` | `2201` | `staging-bastion` | `~/.ssh/keys/staging_ed25519` | `accept-new` |
   | `legacy-reports` | `reports.legacy.internal` | `reports` | `2200` | none | `~/.ssh/keys/legacy_rsa` | `true` |

3. The legacy host must also keep these compatibility additions in its effective
   config:
   - `HostKeyAlgorithms +ssh-rsa`
   - `PubkeyAcceptedAlgorithms +ssh-rsa`
   - `KexAlgorithms +diffie-hellman-group14-sha1`

4. Permissions must be tightened:
   - `/home/user/.ssh` mode `700`
   - `/home/user/.ssh/config` mode `600`
   - every file under `/home/user/.ssh/conf.d` mode `600`
   - every file under `/home/user/.ssh/keys` mode `600`

5. Create `/home/user/.ssh/effective_hosts.tsv`. It must contain exactly one
   header line followed by one line for each alias in the order shown above.
   Columns are tab-separated:

   ```text
   alias	hostname	user	port	proxyjump	identityfile	stricthostkeychecking
   ```

   Use `-` for aliases that have no `proxyjump`. The values in this TSV must be
   derived from the repaired effective OpenSSH configuration, preserving the
   normalized values printed by `ssh -G`.

Do not contact any SSH server. This task is entirely local.
