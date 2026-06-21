FROM ubuntu:22.04

# Update package list and install Python & pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the student test-suite
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create initial filesystem state required by the exercise
# ------------------------------------------------------------------
# 1. Base directory for the fictitious user
RUN mkdir -p /home/user

# 2. Source logs directory with exact file contents
RUN mkdir -p /home/user/migration_logs

RUN cat > /home/user/migration_logs/day1.log <<'EOF'
auth
billing
auth
user
search
billing
auth
cdn
EOF

RUN cat > /home/user/migration_logs/day2.log <<'EOF'
search
video
auth
search
billing
user
video
video
cdn
EOF

RUN cat > /home/user/migration_logs/day3.log <<'EOF'
auth
billing
search
search
cdn
cdn
billing
auth
video
video
analytics
EOF

# 3. Destination directory for the report (empty for now)
RUN mkdir -p /home/user/migration_summary

# 4. Permissions: directories 755, files 644
RUN find /home/user -type d -exec chmod 755 {} + && \
    find /home/user -type f -exec chmod 644 {} +

# This container image provides the starting filesystem state required for
# the "service frequency" migration-logs exercise.
# It includes:
#   • /home/user/migration_logs with three pre-populated log files.
#   • An (empty) /home/user/migration_summary directory where the student
#     will write service_frequency_20240101.csv.
#   • Python 3 and pytest installed for automated grading.