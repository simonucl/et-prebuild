# Author="Apptainer Task Prep Bot"
# Description="Container for CPU/memory snapshot exercise with pytest pre-installed."
# Help:
#   This container provides the starting environment for the CPU/memory
#   profiling exercise. It includes:
#     - /home/user/apps/cpu_hog.py – CPU burner script
#     - pytest – installed for the grading suite
#   Work must be done from an unprivileged shell after the container is built.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        psmisc \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/apps

RUN cat <<'EOF' > /home/user/apps/cpu_hog.py
#!/usr/bin/env python3
import math, time
while True:
    x = math.sqrt(98765.4321) ** 2      # pointless calculation
EOF

RUN chmod 0755 /home/user/apps/cpu_hog.py

RUN chmod 0777 /home/user

RUN chmod 755 /home/user