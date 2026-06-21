FROM ubuntu:22.04

# Author: Automated build
# Description: Environment for sed/awk workflow exercise with pytest pre-installed
LABEL Author="Automated build" \
      Description="Environment for sed/awk workflow exercise with pytest pre-installed"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/work/raw

RUN cat > /home/user/work/raw/employee_records.csv <<'CSV_EOF'
#id,name,department,salary,join_date
101,Alice Johnson,Engineering,95000,2015-03-12
102,Bob Smith,Sales,70000,2016-07-19
103,Charlie King,Engineering,105000,2014-11-02
104,Denise Wu,HR,65000,2018-04-23
105,Evan Li,Engineering,99000,2017-09-14
106,Farah Ali,Marketing,72000,2019-12-01
107,George Brown,Engineering,88000,2020-05-30
108,Helen Clark,Sales,73000,2013-01-25

CSV_EOF

RUN chmod 644 /home/user/work/raw/employee_records.csv && \
    chmod 755 /home/user /home/user/work /home/user/work/raw