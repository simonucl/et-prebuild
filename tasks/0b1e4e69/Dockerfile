# Author ToyCI Builder
# Description Environment for Makefile-based CI/CD exercise
FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project && \
    chmod -R 0777 /home/user && \
    rm -f /home/user/project/ci_report.txt

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Equivalent of runscript
CMD echo "Container for Toy CI/CD assignment." && \
    echo "You probably want to 'exec' into the container and work under /home/user/project."

# Help section
# This container provides everything needed for the Toy CI/CD Makefile exercise:
# - GNU Make
# - Python 3
# - Pytest (used by the autograder)
# The project skeleton lives in /home/user/project.
# Start by adding a Makefile there, then run:
#     make -C /home/user/project ci