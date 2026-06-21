# syntax=docker/dockerfile:1
# This container sets up the initial filesystem and data required for the
# “behavioral_study” organizational task. It installs pytest and places three
# TSV files in /home/user/downloads while leaving
# /home/user/projects/behavioral_study/ absent so that learners can complete
# the exercise.
# Author behavioral-study-task-initializer

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/downloads && \
    mkdir -p /home/user/projects

RUN cat <<'EOF' > /home/user/downloads/demographics.tsv
id	age	gender
1	34	F
2	29	M
EOF

RUN cat <<'EOF' > /home/user/downloads/reaction_times.tsv
participant_id	time_ms
1	532
2	489
EOF

RUN cat <<'EOF' > /home/user/downloads/survey_responses.tsv
pid	q1	q2	q3
1	4	3	5
2	5	4	4
EOF

RUN chmod -R a+rwx /home/user && chmod 755 /home/user

LABEL Author="behavioral-study-task-initializer"