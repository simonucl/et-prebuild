FROM ubuntu:22.04

# Labels
LABEL Author="On-call Support Engineer"
LABEL Description="Initial state for diagnostics-collection task"

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial pipeline log files expected by the tests
RUN mkdir -p /home/user/pipeline/logs

RUN printf "[2023-01-01 00:00:01] ERROR Pipeline crashed at step 3\n" \
    > /home/user/pipeline/logs/error.log

RUN printf "[2023-01-01 00:00:00] INFO  Pipeline started\n" \
    > /home/user/pipeline/logs/pipeline.log

# Ensure the unprivileged runtime user can read/write these files
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV PYTHONUNBUFFERED=1