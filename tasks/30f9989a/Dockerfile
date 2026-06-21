FROM ubuntu:22.04

# Help / labels
# DNS audit harness container. Files are located in /home/user/dba_dns_check.
LABEL Author="GPT-4 Apptainer Builder"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -eux && mkdir -p /home/user/dba_dns_check

RUN cat << 'EOF' > /home/user/dba_dns_check/host_targets.lst
db-primary.internal
db-replica.internal
analytics-db.internal
EOF

RUN cat << 'EOF' > /home/user/dba_dns_check/run_check.sh
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST_FILE="$SCRIPT_DIR/host_targets.lst"
OUTPUT_FILE="$SCRIPT_DIR/dns_check_report.log"
TIMESTAMP="2023-01-01T00:00:00Z"

: > "$OUTPUT_FILE"

while IFS= read -r host; do
  [[ -z "$host" ]] && continue
  ips=$(getent ahosts "$host" 2>/dev/null | awk '{print $1}' | sort -u | paste -sd " " || true)
  if [[ -z "$ips" ]]; then
    echo "$TIMESTAMP $host UNRESOLVED" >> "$OUTPUT_FILE"
  else
    echo "$TIMESTAMP $host $ips" >> "$OUTPUT_FILE"
  fi
done < "$HOST_FILE"

exit 0
EOF

RUN chmod +x /home/user/dba_dns_check/run_check.sh

RUN /home/user/dba_dns_check/run_check.sh

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD echo "DNS audit harness container. Files are located in /home/user/dba_dns_check."