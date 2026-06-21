FROM ubuntu:22.04

# Basic tooling
RUN set -eux && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state expected by the tests
# Create the canonical /home/user tree
RUN mkdir -p /home/user/temp

# Give write-access to any (non-root) user so the learner can create
# new sub-directories such as /home/user/cloud_reports later on.
RUN chmod 0777 /home/user

# Directory that must exist before the learner starts
RUN chmod 0755 /home/user/temp

# CSV file with the exact required contents
RUN cat > /home/user/temp/cost_report_Q42023.csv <<'EOF'
month,total_spend_usd
Oct,12345.67
Nov,11001.22
Dec,12999.00
EOF

# Ensure correct permissions
RUN chmod 0644 /home/user/temp/cost_report_Q42023.csv

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Default entrypoint: open an interactive shell
CMD ["/bin/bash", "-l"]

# Help:
# This container supplies the initial environment for the FinOps
# consolidation exercise.  It already contains:
#
#   • /home/user/temp/
#   • /home/user/temp/cost_report_Q42023.csv
#
# Use standard Unix commands to move and rename the CSV, create the
# symlink, and write the audit log as described in the task instructions.