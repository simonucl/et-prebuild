FROM ubuntu:22.04

# Help text
# This container provides the baseline filesystem and pytest installation
# required for the cron-policy exercise.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/policies && \
    mkdir -p /home/user/cron && \
    mkdir -p /home/user/logs

RUN WEEKLY_LINE="0 0 * * 0 /home/user/scripts/weekly_maintenance.sh" && \
    echo "${WEEKLY_LINE}" > /home/user/policies/allowed_cron_jobs.txt && \
    echo "${WEEKLY_LINE}" > /home/user/cron/enforced_user_crontab

RUN chmod 0777 /home/user /home/user/policies /home/user/cron /home/user/logs && \
    chmod 0666 /home/user/policies/allowed_cron_jobs.txt && \
    chmod 0666 /home/user/cron/enforced_user_crontab

# Labels from definition file
LABEL Author="ChatGPT DevSecOps Container Builder"
LABEL Description="Container for cron-policy assessment task (includes pytest)"