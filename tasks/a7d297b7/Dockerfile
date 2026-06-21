# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="Automation Workflow Prep"
# Description="Container with initial CSV data and pytest installed for the workflow automation assignment."

ENV PATH="/usr/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data

RUN cat <<'EOF' > /home/user/data/employees.csv
id,name,department,hire_date
1,Alice Zephyr,Engineering,2019-03-14
2,Bob Yellow,Sales,2018-07-22
3,Charlie Xander,Engineering,2020-11-03
4,Diana White,HR,2017-01-30
5,Edward Violet,Engineering,2016-05-12
6,Frida Umber,Sales,2021-09-08
EOF

RUN cat <<'EOF' > /home/user/data/salaries.csv
id,year,amount
1,2021,68000
1,2022,72000
2,2022,69000
3,2022,88000
4,2022,65000
5,2021,70000
5,2022,91000
6,2022,73000
EOF

RUN chmod 644 /home/user/data/*.csv