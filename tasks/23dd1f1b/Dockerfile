# Container prepared for the “periodic housekeeping” assignment.
# All initial *.perf files, directories and permissions are set up,
# and pytest is installed for the automated grader.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/user

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip gzip coreutils findutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/benchmarks/app1/profiles \
             /home/user/projects/benchmarks/app2/perf_logs \
             /home/user/projects/benchmarks/legacy \
             /home/user/projects/benchmarks/newapp

RUN cat <<'EOF' > /home/user/projects/benchmarks/app1/profiles/2023-01-15_run1.perf
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
PERF SAMPLE DATA FILE 1
EOF

RUN cat <<'EOF' > /home/user/projects/benchmarks/app2/perf_logs/performance.perf
# callgraph-flat
# event: cycles:u
# captured on CI runner
0.01  sys_openat
0.02  sys_read
0.97  app_compute
EOF

RUN cat <<'EOF' > /home/user/projects/benchmarks/legacy/old_perf.perf
Legacy profiling dump
time=12345, cycles=67890
branch-misses=1024

EOF

RUN printf 'EOF\n' >> /home/user/projects/benchmarks/legacy/old_perf.perf

RUN echo 'Raw profile – keep this one uncompressed!' > /home/user/projects/benchmarks/newapp/newrun.perf

RUN echo 'This directory holds profiling output for app1.' > /home/user/projects/benchmarks/app1/readme.txt

RUN touch -d "2023-02-01 12:00:00" /home/user/projects/benchmarks/app1/profiles/2023-01-15_run1.perf && \
    touch -d "2023-02-01 12:00:00" /home/user/projects/benchmarks/app2/perf_logs/performance.perf && \
    touch -d "2023-02-01 12:00:00" /home/user/projects/benchmarks/legacy/old_perf.perf

RUN mkdir -p /home/user/archival_logs

RUN chmod -R a+rwx /home/user

# Labels
# Author: LearningContainerBot
# Project: Perf-housekeeping-initial-state