FROM ubuntu:22.04

# Labels
LABEL Author="backup-task-setup"
LABEL Description="Initial state for the weekly backup reporting exercise"

# Help information (as comments):
# This container image provides the initial filesystem layout needed for the
# "weekly PostgreSQL backup report" assignment.  It contains:
#
#   • /home/user/backups   – 14 nightly CSV files (primary + replica for
#                             2023-06-18 through 2023-06-24)
#   • Python 3 and pytest  – available for the autograder to validate both the
#                             initial and final states of the exercise.
#
# The /home/user/reports directory is intentionally **absent** so the student
# solution can create it and place their deliverables there.

ENV DEBIAN_FRONTEND=noninteractive

# Basic tooling: Python + pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Directory structure for the assignment
RUN mkdir -p /home/user/backups && \
    chmod 755 /home/user /home/user/backups

# Create CSV files for primary_backup_20230618.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-18,primary-db,83,1225,17m50s" \
    > /home/user/backups/primary_backup_20230618.csv && \
    chmod 644 /home/user/backups/primary_backup_20230618.csv

# Create CSV files for replica_backup_20230618.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-18,replica-db,00:15:10,00:37:01,SUCCESS" \
    > /home/user/backups/replica_backup_20230618.csv && \
    chmod 644 /home/user/backups/replica_backup_20230618.csv

# Create CSV files for primary_backup_20230619.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-19,primary-db,84,1230,18m02s" \
    > /home/user/backups/primary_backup_20230619.csv && \
    chmod 644 /home/user/backups/primary_backup_20230619.csv

# Create CSV files for replica_backup_20230619.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-19,replica-db,00:15:15,00:37:10,SUCCESS" \
    > /home/user/backups/replica_backup_20230619.csv && \
    chmod 644 /home/user/backups/replica_backup_20230619.csv

# Create CSV files for primary_backup_20230620.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-20,primary-db,85,1240,18m15s" \
    > /home/user/backups/primary_backup_20230620.csv && \
    chmod 644 /home/user/backups/primary_backup_20230620.csv

# Create CSV files for replica_backup_20230620.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-20,replica-db,00:15:18,00:37:20,SUCCESS" \
    > /home/user/backups/replica_backup_20230620.csv && \
    chmod 644 /home/user/backups/replica_backup_20230620.csv

# Create CSV files for primary_backup_20230621.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-21,primary-db,86,1248,18m18s" \
    > /home/user/backups/primary_backup_20230621.csv && \
    chmod 644 /home/user/backups/primary_backup_20230621.csv

# Create CSV files for replica_backup_20230621.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-21,replica-db,00:15:20,00:37:25,SUCCESS" \
    > /home/user/backups/replica_backup_20230621.csv && \
    chmod 644 /home/user/backups/replica_backup_20230621.csv

# Create CSV files for primary_backup_20230622.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-22,primary-db,85,1245,18m19s" \
    > /home/user/backups/primary_backup_20230622.csv && \
    chmod 644 /home/user/backups/primary_backup_20230622.csv

# Create CSV files for replica_backup_20230622.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-22,replica-db,00:15:22,00:37:30,SUCCESS" \
    > /home/user/backups/replica_backup_20230622.csv && \
    chmod 644 /home/user/backups/replica_backup_20230622.csv

# Create CSV files for primary_backup_20230623.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-23,primary-db,85,1249,18m20s" \
    > /home/user/backups/primary_backup_20230623.csv && \
    chmod 644 /home/user/backups/primary_backup_20230623.csv

# Create CSV files for replica_backup_20230623.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-23,replica-db,00:15:24,00:37:35,SUCCESS" \
    > /home/user/backups/replica_backup_20230623.csv && \
    chmod 644 /home/user/backups/replica_backup_20230623.csv

# Create CSV files for primary_backup_20230624.csv
RUN printf '%s\n' \
    "Date,Hostname,Tables_Backup,Size_MB,Duration" \
    "2023-06-24,primary-db,85,1250,18m23s" \
    > /home/user/backups/primary_backup_20230624.csv && \
    chmod 644 /home/user/backups/primary_backup_20230624.csv

# Create CSV files for replica_backup_20230624.csv
RUN printf '%s\n' \
    "Date,Hostname,Copy_Start,Copy_End,Status" \
    "2023-06-24,replica-db,00:15:26,00:37:45,SUCCESS" \
    > /home/user/backups/replica_backup_20230624.csv && \
    chmod 644 /home/user/backups/replica_backup_20230624.csv

WORKDIR /home/user