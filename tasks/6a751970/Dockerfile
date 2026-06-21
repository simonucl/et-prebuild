# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python, pip, locales, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial directory structure and source TSV files
# ------------------------------------------------------------------
RUN mkdir -p /home/user/datasets

# ----- 2022 dataset ------------------------------------------------
RUN cat > /home/user/datasets/survey_2022.tsv <<'EOF'
id	name	age	gender	country	income	hired_date
101	Anna	28	F	USA	65000	2021-05-10
102	Ben	34	M	Canada	72000	2019-09-13
103	Chloé	25	F	France	58000	2020-06-22
104	David	40	M	USA	80000	2018-02-14
105	Ella	31	F	UK	69000	2022-01-03
EOF

# ----- 2023 dataset ------------------------------------------------
RUN cat > /home/user/datasets/survey_2023.tsv <<'EOF'
id	name	department	satisfaction_score	promotion_eligible
101	Anna	Sales	4	Yes
102	Ben	Marketing	5	No
103	Chloé	Support	3	Yes
104	David	Engineering	4	No
105	Ella	HR	5	Yes
EOF

# Permissions: world-readable, no execute bits
RUN chmod 644 /home/user/datasets/survey_2022.tsv && \
    chmod 644 /home/user/datasets/survey_2023.tsv

# Ensure home directory permissions
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Do NOT create /home/user/cleaned yet – the learner will.