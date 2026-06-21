# Converted from Apptainer definition
FROM ubuntu:22.04

# Help text
# This Apptainer image provides the initial environment for the
# "performance-summary" shell task. It includes:
#   • /home/user/analytics/query_perf_2023.csv with correct data
#   • Required directory permissions
#   • Python 3 and pytest pre-installed for automated grading

# Environment variables
ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/analytics && \
    chmod 755 /home/user/analytics

RUN cat <<'CSVEND' > /home/user/analytics/query_perf_2023.csv
query_id,sql_text,execution_time_ms,rows_examined,rows_returned
Q1001,SELECT * FROM users,45,1200,100
Q1002,DELETE FROM sessions WHERE expired=1,30,8000,0
Q1003,UPDATE orders SET status='shipped' WHERE id=24,52,1,0
Q1004,SELECT COUNT(*) FROM logs,120,1500000,1
Q1005,INSERT INTO products(name,price) VALUES('Widget',9.99),10,0,1
CSVEND

RUN chmod 644 /home/user/analytics/query_perf_2023.csv