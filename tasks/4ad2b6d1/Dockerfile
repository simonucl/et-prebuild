FROM ubuntu:22.04

# Help text
# This Apptainer container provides the raw datasets located at:
#   /home/user/datasets/raw/
#
# A writable directory for cleaned outputs is located at:
#   /home/user/datasets/clean/
#
# Pytest is pre-installed for the grading suite.

LABEL Author="Data-Engineer-Bot"
LABEL Description="Container with raw demo datasets and pytest pre-installed."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/datasets/raw && \
    mkdir -p /home/user/datasets/clean

RUN cat >/home/user/datasets/raw/transactions.csv <<'CSV'
transaction_id,date,amount,user_id,currency
1001,01/02/2022,23.5,501,USD
1002,2022-01-03,15.0,502,USD
1003,01-04-2022,12.99,,USD
1002,2022-01-03,15.0,502,USD
1004,04/01/2022,20,503,usd
1005,2022/01/05,7.5,504,USD
CSV

RUN cat >/home/user/datasets/raw/users.json <<'JSON'
[
 {"user_id":501,"name":"Alice","email":"alice@example.com"},
 {"user_id":502,"name":"Bob","email":"bob@example.com"},
 {"user_id":503,"name":"Charlie"},
 {"user_id":504,"name":"David","email":"david@example.com"},
 {"user_id":504,"name":"David Duplicate","email":"david@example.com"}
]
JSON

RUN chmod -R 0777 /home/user/datasets/clean

ENV PATH="$PATH:$HOME/.local/bin"
ENV HOME=/home/user

RUN chmod 755 /home/user