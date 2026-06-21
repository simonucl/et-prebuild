# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author incident-triage-container

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/incident_triage/input

RUN cat > /home/user/incident_triage/input/solver_a.log <<'EOF'
[INFO] Solver: OptiMax v2.0
[START] 2023-02-04T12:00:00Z
status=OPTIMAL
iterations=145
objective=1234.5678
solve_time_sec=2.345
[END] 2023-02-04T12:00:02Z
EOF

RUN cat > /home/user/incident_triage/input/solver_b.log <<'EOF'
[INFO] Solver: OptiMax v2.0
[START] 2023-02-04T12:05:00Z
status=INFEASIBLE
iterations=87
objective=nan
solve_time_sec=1.230
[END] 2023-02-04T12:05:02Z
EOF

RUN cat > /home/user/incident_triage/input/solver_c.log <<'EOF'
[INFO] Solver: OptiPlus v1.4
[START] 2023-02-04T12:10:00Z
status=TIME_LIMIT
iterations=1000
objective=99999.999
solve_time_sec=60.000
[END] 2023-02-04T12:11:00Z
EOF

RUN chmod -R 777 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user