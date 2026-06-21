FROM ubuntu:22.04

# Image help:
# This container image provides the initial filesystem and toolchain state for
# the profiling exercise.
# Pre-created resources:
#   /home/user/apps/cpu_stress.py
#   /home/user/apps/io_stress.py
#   /home/user/profiles/  (writable)
# Available profiling utilities:
#   /usr/bin/time  (GNU time)
#   strace -c
# Python 3 and pytest are installed system‑wide.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        strace \
        time && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/apps && \
    mkdir -p /home/user/profiles && \
    chmod 0777 /home/user/profiles

RUN cat >/home/user/apps/cpu_stress.py <<'PYCPU'
#!/usr/bin/env python3
import math

def busy():
    total = 0
    for i in range(5_000_00):  # Five-hundred thousand iterations
        total += math.sqrt(i)
    print(total)

if __name__ == "__main__":
    busy()
PYCPU

RUN cat >/home/user/apps/io_stress.py <<'PYIO'
#!/usr/bin/env python3
import os, tempfile

def thrash():
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "w+b") as f:
        for i in range(1000):
            f.write(b"x" * 4096)
        f.flush()
        os.fsync(f.fileno())
    os.remove(path)

if __name__ == "__main__":
    thrash()
PYIO

RUN chmod 0755 /home/user/apps/cpu_stress.py /home/user/apps/io_stress.py

ENV PATH="/home/user/apps:${PATH}"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user

LABEL Author="OpenAI"
LABEL Description="Environment for concurrent profiling task with pre-seeded workloads"
LABEL Version="1.0"