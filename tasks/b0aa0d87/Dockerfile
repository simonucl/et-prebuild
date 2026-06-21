FROM ubuntu:22.04

# Make sure Python and pip are on PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    echo "Updating package list and installing Python + pytest..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating directory structure under /home/user ..." && \
    mkdir -p /home/user/backup_source/images && \
    mkdir -p /home/user/backup_target

# finance_2021.csv – 3 lines, each ending with a newline
RUN cat > /home/user/backup_source/finance_2021.csv <<'EOF'
Finance Data 2021
ID,Amount
1,1000
EOF

# brand_logo.png – literal 7-byte content "PNGDATA"
RUN printf 'PNGDATA' > /home/user/backup_source/images/brand_logo.png

RUN echo "Creating symbolic links inside backup_target ..." && \
    ln -s ../backup_source/finance_2021.csv             /home/user/backup_target/finance_2021.csv && \
    ln -s ../backup_source/images/logo.png              /home/user/backup_target/logo.png && \
    ln -s ../backup_source/reports/report_q1.txt        /home/user/backup_target/old_report.txt

RUN echo "Setting permissions ..." && \
    chmod 755 /home/user /home/user/backup_source /home/user/backup_source/images /home/user/backup_target && \
    chmod 644 /home/user/backup_source/finance_2021.csv /home/user/backup_source/images/brand_logo.png && \
    echo "Initial state prepared."

# This container sets up the initial filesystem state for the backup-integrity
# exercise.  It installs Python 3 and pytest for automated evaluation and
# prepares the required directories, files, and (intentional) broken
# symlinks under /home/user.

CMD ["echo", "Container for backup-integrity exercise.  Use this as a build image; it does not execute anything by default."]