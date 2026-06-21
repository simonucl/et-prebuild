FROM ubuntu:22.04

# Update base system and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Create the initial directory / file structure for the exercise
RUN mkdir -p /home/user/db_backups/archive

RUN echo "placeholder text" > /home/user/db_backups/prod_full_2023-12-31.sql.gz
RUN echo "placeholder text" > /home/user/db_backups/prod_inc_2024-01-01.sql.gz
RUN echo "placeholder text" > /home/user/db_backups/prod_inc_2024-01-02.sql.gz

RUN touch /home/user/db_backups/archive/prod_full_2023-12-30.sql.gz

RUN printf "Backups are dumped nightly.\n" > /home/user/db_backups/readme.txt

RUN printf "2024-02-15_10:00:00 moved 2 files\n2024-02-16_10:00:00 moved 1 files\n" \
    > /home/user/db_backups/backup_move.log

# Ensure the on-call engineer (non-root runtime user) can modify files
RUN chmod -R 777 /home/user/db_backups

# Environment settings
ENV PATH="$PATH:/home/user/.local/bin"

RUN chmod 755 /home/user

LABEL Author="db-reliability-task"
LABEL Description="Initial state for backup move & log exercise (pytest ready)"