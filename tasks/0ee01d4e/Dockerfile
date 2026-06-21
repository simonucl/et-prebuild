FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Set up initial filesystem state
RUN mkdir -p /home/user/exp_runs/run_01 && \
    mkdir -p /home/user/exp_runs/run_02

RUN printf "run_01\nrun_02\n" > /home/user/exp_runs/run_list.txt

RUN : > /home/user/exp_runs/run_01/model.bin

RUN chmod -R a+rwx /home/user

# Apply environment chmod from %environment
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Help text
# This container provides the starting environment for the “mini artifact-tracking”
# exercise. It includes:
#  • pytest (for autograding)
#  • The predefined /home/user/exp_runs/ directory structure exactly as required.
# The /home/user/artifact_store/ directory is intentionally NOT created;
# students must generate it during their solution.