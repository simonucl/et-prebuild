FROM ubuntu:22.04

# Update APT index and install Python + pip
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip
RUN pip3 install --no-cache-dir pytest

# Create /home/user and set permissions
RUN mkdir -p /home/user
RUN chmod 0777 /home/user

# Create the raw log with exact contents
RUN cat > /home/user/repo-activity.log <<'EOF'
2023-08-14 21:34:11 libs-release com.example:foo:0.9.0 UPLOAD
2023-08-15 00:05:22 libs-snapshot com.example:bar:2.0.0-SNAPSHOT UPLOAD
2023-08-15 01:45:10 libs-release com.example:foo:1.0.0 UPLOAD
2023-08-15 02:10:05 libs-release com.example:foo:1.0.0 DELETE
2023-08-15 08:22:33 plugins-release com.company:plugin:3.1.4 UPLOAD
2023-08-15 09:10:00 plugins-release com.company:plugin:3.1.3 DELETE
2023-08-16 10:00:00 libs-snapshot com.example:bar:2.0.1-SNAPSHOT UPLOAD
EOF

# Ensure log readable by all but not writable by others
RUN chmod 0666 /home/user/repo-activity.log

# Environment adjustments
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
RUN chmod 755 /home/user

# Labels
LABEL Author="OpenAI ChatGPT – Apptainer build file for repo-activity summary task"

# Help text (as comments)
# This container contains the initial state for the
# “Generate a daily repository-activity summary” task.
# /home/user/repo-activity.log – raw activity log
# Students will create /home/user/daily_summary_2023-08-15.txt
# Python 3 and pytest are pre-installed.

# Run script equivalent
CMD echo "This container is prepared for the repo-activity summary task." && \
    echo "Enter the container and create the required summary file."