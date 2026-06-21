FROM ubuntu:22.04

# Labels
LABEL Author="QA-Automation Setup"
LABEL Description="Container prepared for the critical scenario summary task."

# Install requirements
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory tree and permissions
RUN mkdir -p /home/user/projects/qa/test_scenarios && \
    mkdir -p /home/user/projects/qa/reports && \
    mkdir -p /home/user/projects/qa/work && \
    chmod -R 777 /home/user/projects/qa/reports && \
    chmod -R 777 /home/user/projects/qa/work

# Create the input CSV file with the exact content
RUN cat > /home/user/projects/qa/test_scenarios/scenarios.csv <<'EOF'
id,title,severity,status,owner
1,"Login with invalid password",low,closed,alice
2,"Login with valid password",medium,closed,bob
15,"Password reset email not sent",high,open,carol
23,"Profile picture upload fails",medium,open,alice
42,"Database deadlock during signup",critical,open,dave
55,"Race condition on logout",critical,closed,emma
71,"Session not terminated on password change",high,open,bob
85,"Crash on importing malformed CSV",critical,reopened,carol
104,"System reboot on malformed packet",critical,open,emma
175,"Two-factor code not accepted",high,open,dave
200,"Memory leak in report generator",critical,in-progress,frank
EOF

# Ensure the CSV is world-readable
RUN chmod 644 /home/user/projects/qa/test_scenarios/scenarios.csv

# Set permissions on home directory
RUN chmod 755 /home/user