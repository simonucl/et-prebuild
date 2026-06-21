# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up initial filesystem state
RUN mkdir -p /home/user/infra

# Create config files with 2022 passwords
RUN printf 'username=db_user\npassword=db_pass_2022\n' > /home/user/infra/db.cfg
RUN printf 'username=redis_user\npassword=redis_pass_2022\n' > /home/user/infra/redis.cfg
RUN printf 'username=api_user\npassword=api_pass_2022\n' > /home/user/infra/api.cfg

# Permissions
RUN chmod -R 0777 /home/user

# Environment variables
ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8