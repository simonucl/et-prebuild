FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Task="On-prem ETL debug environment"
LABEL Purpose="Provide initial failing state for learner to fix"

# Environment variables
ENV PYTHONUNBUFFERED=1

# 1. Base tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# 2. Prepare initial ETL workspace
RUN mkdir -p /home/user/etl/input /home/user/etl/output /home/user/etl/config /home/user/etl/logs

# Seed input data
RUN cat > /home/user/etl/input/input_data.csv <<'CSV'
id,name
1,Alice
CSV

# Faulty YAML configuration (as described in the task)
RUN cat > /home/user/etl/config/job_config.yaml <<'YAML'
# Nightly ETL job configuration (intentionally incorrect)
delimiter: ";"
YAML

# Historical log containing the delimiter error
RUN cat > /home/user/etl/logs/etl_2023-01-01.log <<'LOG'
2023-01-01T00:00:01Z INFO  Starting ETL job
2023-01-01T00:00:02Z ERROR DelimiterMismatchError: expected ';' but found ',' on line 1
LOG

# 3. Permissions: make everything modifiable by the (non-root) runtime user
RUN chmod -R 0777 /home/user/etl && \
    chmod 755 /home/user