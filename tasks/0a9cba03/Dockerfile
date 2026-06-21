FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem state
RUN mkdir -p /home/user/test_env && \
    chmod 0777 /home/user/test_env

# Create qa_cases.log with required contents
RUN cat > /home/user/test_env/qa_cases.log <<'EOF'
SEC_Login
SEC_Login
SEC_Logout
UI_Homepage_Load
UI_Homepage_Load
UI_Homepage_Load
API_GetUser
API_GetUser
API_GetUser
API_GetUser
EOF

RUN chmod 0644 /home/user/test_env/qa_cases.log

# Ensure output file does not exist
RUN rm -f /home/user/test_env/freq_report.txt

# Ensure /home/user has correct permissions
RUN mkdir -p /home/user && chmod 755 /home/user

LABEL Author="task-setup"
LABEL Description="Initial environment for QA log frequency report task"