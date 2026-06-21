FROM ubuntu:22.04

# Ensure python and pip in PATH
ENV PATH="$PATH:/usr/bin"

# Author="Generated for legacy-analytics task"
# Description="Container prepared for the legacy-analytics educational task (pytest included)"

RUN set -e && apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip ca-certificates && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/legacy-analytics

RUN cat >/home/user/legacy-analytics/tracker.py <<'PYEOF'
#!/usr/bin/env python3
print("legacy-analytics OK")
PYEOF

RUN chmod 755 /home/user/legacy-analytics && chmod 755 /home/user/legacy-analytics/tracker.py

RUN chown -R root:root /home/user 2>/dev/null || true