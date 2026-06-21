FROM ubuntu:22.04

# Container for the “Filter Research Upload Logs with a Single Regex Command” task.
# Pre-installs pytest and prepares the initial access.log file required by the assessment.
# Author: edu-setup
# Description: Environment for filtering log task with pytest pre-installed.

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/datasets

RUN cat > /home/user/datasets/access.log <<'EOF'
[2024-03-01 10:15:00] DATASET:climate_arctic_ice UPLOADED BY alice STATUS 201 TIME 456
[2024-03-01 10:17:42] DATASET:geology_rock_layers UPLOADED BY bob STATUS 201 TIME 512
[2024-03-02 09:03:11] DATASET:climate_global_temp UPLOADED BY carol STATUS 500 TIME 789
[2024-03-02 11:45:33] DATASET:climate_atmos_CO2 UPLOADED BY dave STATUS 201 TIME 300
[2024-03-02 12:00:00] DATASET:biology_cell_images UPLOADED BY eve STATUS 201 TIME 102
[2024-03-03 08:20:20] DATASET:climate_ocean_salinity UPLOADED BY frank STATUS 201 TIME 402
[2024-03-03 09:10:05] DATASET:climate_arctic_ice UPLOADED BY alice STATUS 404 TIME 150
[2024-03-03 10:11:11] DATASET:physics_particle_tracks UPLOADED BY grace STATUS 201 TIME 250
EOF

RUN chmod -R 0777 /home/user

RUN chmod 755 /home/user