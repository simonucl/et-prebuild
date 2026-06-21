# Help
# This Docker image contains:
# - Python 3 and pytest
# - GNU time with "-f" support
# - GNU parallel
# - Target script at /home/user/scripts/sleep_for.py

FROM ubuntu:22.04

# Environment variables from %environment (none provided)

# %post section
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        time \
        parallel && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/scripts && \
    chmod 0777 /home/user && \
    chmod 0755 /home/user/scripts

RUN cat > /home/user/scripts/sleep_for.py << 'PYEOF'
#!/usr/bin/env python3
import sys, time
if __name__ == "__main__":
    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    time.sleep(secs)
PYEOF

RUN chmod 0755 /home/user/scripts/sleep_for.py

# From %labels: convert chmod to RUN, other entries to LABEL
RUN chmod 755 /home/user

LABEL Author="benchmark-setup"
LABEL Description="Container prepared for benchmarking task with GNU time, GNU parallel, pytest, and target script."