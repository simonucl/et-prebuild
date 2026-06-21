# Converted from Apptainer definition file
FROM ubuntu:22.04

# Base tools and Python/pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Initial dataset setup
RUN mkdir -p /home/user/data_to_archive/docs && \
    mkdir -p /home/user/data_to_archive/media && \
    printf 'Quarterly Report Q1 2024\n' > /home/user/data_to_archive/docs/report1.txt && \
    printf 'Quarterly Report Q2 2024\n' > /home/user/data_to_archive/docs/report2.txt && \
    printf 'FAKEJPEGDATA\n' > /home/user/data_to_archive/media/image1.jpg && \
    printf 'FAKEMP4DATA\n' > /home/user/data_to_archive/media/video1.mp4 && \
    chmod -R a+rX,ug+w /home/user/data_to_archive && \
    if [ -d /home/user/backups ]; then rm -rf /home/user/backups; fi

# Environment setup
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run script
CMD echo "Apptainer container ready for the backup task."