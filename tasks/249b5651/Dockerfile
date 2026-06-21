# Author example
# Description "Container pre-populated with CI/CD metrics artefacts and pytest"

FROM ubuntu:22.04

ENV PATH="/usr/local/bin:/usr/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cicd_db_work

RUN cat > /home/user/cicd_db_work/cicd_sql_audit.log <<'EOF'
CREATE TABLE build_metrics (id INTEGER PRIMARY KEY, pipeline_name TEXT NOT NULL, status TEXT CHECK(status IN ('success','failed')) NOT NULL, build_time_seconds INTEGER NOT NULL, build_date DATE NOT NULL);
INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (1,'web-frontend','success',420,'2023-09-01');
INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (2,'api-service','failed',370,'2023-09-01');
INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (3,'database-migrations','success',255,'2023-09-02');
EOF

RUN sqlite3 /home/user/cicd_db_work/ci_cd_metrics.db <<'SQL'
CREATE TABLE build_metrics (id INTEGER PRIMARY KEY, pipeline_name TEXT NOT NULL, status TEXT CHECK(status IN ('success','failed')) NOT NULL, build_time_seconds INTEGER NOT NULL, build_date DATE NOT NULL);
INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (1,'web-frontend','success',420,'2023-09-01');
INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (2,'api-service','failed',370,'2023-09-01');
INSERT INTO build_metrics (id, pipeline_name, status, build_time_seconds, build_date) VALUES (3,'database-migrations','success',255,'2023-09-02');
SQL

RUN AVG_VALUE=$(sqlite3 /home/user/cicd_db_work/ci_cd_metrics.db "SELECT ROUND(AVG(build_time_seconds),2) FROM build_metrics;") && \
    printf 'average_build_time_seconds:%s\n' "${AVG_VALUE}" > /home/user/cicd_db_work/build_time_average.txt && \
    chmod 755 /home/user

RUN sqlite3 -header -csv /home/user/cicd_db_work/ci_cd_metrics.db \
        "SELECT id, pipeline_name, status, build_time_seconds, build_date FROM build_metrics ORDER BY id;" \
        > /home/user/cicd_db_work/metrics_export.csv

RUN chmod -R a+r /home/user/cicd_db_work

CMD echo "Container for CI/CD metrics task ready."