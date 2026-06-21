FROM ubuntu:22.04

# Help / labels
# Author="Container Build Automation"
# Description="Environment for the legacy monitoring consolidation task with pytest pre-installed."
LABEL Author="Container Build Automation"
LABEL Description="Environment for the legacy monitoring consolidation task with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/legacy_tools

RUN cat <<'EOF' > /home/user/legacy_tools/hosts.lst
127.0.0.1
localhost
blackhole.local
EOF
RUN chmod 0644 /home/user/legacy_tools/hosts.lst

RUN cat <<'EOF' > /home/user/legacy_tools/run_checks.sh
#!/usr/bin/env bash
#
# Vintage reachability probe used by ops long ago.
# Usage: ./run_checks.sh <host>
# It prints exactly one line and returns a meaningful exit code.
HOST="$1"

case "$HOST" in
  "127.0.0.1")
        echo "STATUS:UP LATENCY_MS:1"
        exit 0
        ;;
  "localhost")
        echo "STATUS:UP LATENCY_MS:2"
        exit 0
        ;;
  *)
        echo "STATUS:DOWN"
        exit 2
        ;;
esac
EOF
RUN chmod 0755 /home/user/legacy_tools/run_checks.sh

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user