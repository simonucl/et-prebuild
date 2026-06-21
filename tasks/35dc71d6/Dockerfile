FROM ubuntu:22.04

# Help text
# This Apptainer image sets up the initial filesystem state for the
# “compromised crontab” incident-response task and includes pytest so that
# automated tests can validate both the initial and final states.

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/forensics

RUN chmod 0777 /home/user/forensics

RUN printf '*/5 * * * * /home/user/scripts/backup.sh\n0 3 * * * /home/user/scripts/cleanup.sh\n@reboot /home/user/scripts/bitcoin_miner.sh\n' > /home/user/forensics/compromised.cron

RUN chmod 0644 /home/user/forensics/compromised.cron

RUN chmod 755 /home/user

LABEL Author="example"
LABEL Description="Environment for compromised crontab forensic analysis exercise"