FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        && rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Create the base directory structure
RUN mkdir -p /home/user/audit_dir/logs

# Populate the expected regular files
RUN echo "sample configuration" > /home/user/audit_dir/config.cfg

RUN printf '#!/bin/bash\necho "Hello world"\n' > /home/user/audit_dir/run.sh

RUN echo "temporary log data" > /home/user/audit_dir/temp.log

RUN echo "public text file" > /home/user/audit_dir/public.txt

RUN echo "error log entry" > /home/user/audit_dir/logs/error.log

# Set the required permissions
RUN chmod 644 /home/user/audit_dir/config.cfg && \
    chmod 755 /home/user/audit_dir/run.sh && \
    chmod 666 /home/user/audit_dir/temp.log && \
    chmod 666 /home/user/audit_dir/public.txt && \
    chmod 644 /home/user/audit_dir/logs/error.log

# Make /home/user writable by the runtime (non-root) user
RUN chmod 777 /home/user

# Labels
LABEL Author="task-preparation-script"

# Default command
CMD ["/bin/bash"]