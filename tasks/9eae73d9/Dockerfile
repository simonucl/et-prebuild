# Based on localimage bootstrap of ubuntu_22.04.sif
FROM ubuntu:22.04

# %help
# Author: example_builder
# Description: Container for the site_admin preparation task (pytest pre-state included).

ENV PYTHONIOENCODING="utf-8"

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN EXERCISE_ROOT="/home/user/site_admin" && \
    mkdir -p "${EXERCISE_ROOT}/users"

RUN EXERCISE_ROOT="/home/user/site_admin" && \
    printf 'username,uid,group,shell,home_dir,required_packages\n' > "${EXERCISE_ROOT}/new_hires.csv"

RUN EXERCISE_ROOT="/home/user/site_admin" && \
    cat > "${EXERCISE_ROOT}/packages_database.txt" <<'EOF'
bash,5.1-2
coreutils,8.32-4
nano,5.4-2
curl,7.74.0-1
python3,3.9.2-1
EOF

RUN chmod -R 0777 /home/user/site_admin && \
    chmod 755 /home/user

# %runscript (informational only)
# This container is intended for automated testing of the site_admin task.
# Use 'apptainer exec' to enter the environment.