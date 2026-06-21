FROM ubuntu:22.04

# Install Python 3 and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up initial filesystem state expected by the assignment's automated tests
RUN mkdir -p /home/user/profiling

# Helper file: /home/user/profiling/host_targets.txt
RUN printf 'frontend.local\nbackend.local\ndb.local\n' \
    > /home/user/profiling/host_targets.txt

# Helper file: /home/user/profiling/ip_map.txt
RUN printf '192.168.50.10 frontend.local\n192.168.50.20 backend.local\n192.168.50.30 db.local\n' \
    > /home/user/profiling/ip_map.txt

# Ensure the directory is writable by unprivileged users so they
# can create dns_profile.log during the exercise.
RUN chmod 0777 /home/user/profiling && \
    chmod 0666 /home/user/profiling/host_targets.txt /home/user/profiling/ip_map.txt && \
    chmod 755 /home/user

# Keep standard paths; just make sure /usr/local/bin is included.
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH