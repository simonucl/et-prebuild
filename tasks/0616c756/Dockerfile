FROM ubuntu:22.04

# Help text
# This Apptainer image provides the initial filesystem state for the
# “firewall manifest” exercise.
# It already contains:
#   • /home/user/etl_firewall_rules.conf  (one specific line, writable)
# Pytest is installed so the evaluation harness can run.

RUN set -e \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN printf "# ETL Pipeline Firewall Rules\n" > /home/user/etl_firewall_rules.conf \
    && chmod 0666 /home/user/etl_firewall_rules.conf

RUN chmod 755 /home/user

LABEL Author="firewall-task-setup"
LABEL Description="Container for firewall manifest task – includes initial state and pytest"