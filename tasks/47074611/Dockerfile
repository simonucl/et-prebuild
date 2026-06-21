FROM ubuntu:22.04

# Help:
# This Apptainer image provides the initial filesystem state for the QA log
# sanitization task. It contains:
# - /home/user/qa_logs/suite1.log
# - /home/user/qa_logs/suite2.log
# Both files have exact required contents. Directory is writable for creation
# of *_clean.log and summary_report.csv. Python3 and pytest are pre-installed.

LABEL Author="umbraassistant"
LABEL Description="Environment for QA log sanitization task with pytest pre-installed."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales \
        sed \
        gawk && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/qa_logs

RUN cat <<'EOF' > /home/user/qa_logs/suite1.log
[2023-08-12 10:12:01] TEST test_login ..... PASS
[2023-08-12 10:12:02] TEST test_logout ..... FAIL
[2023-08-12 10:12:03] TEST test_signup ..... SKIP
[2023-08-12 10:12:04] TEST test_profile_update ..... PASS
[2023-08-12 10:12:05] TEST test_password_reset ..... PASS
EOF

RUN cat <<'EOF' > /home/user/qa_logs/suite2.log
[2023-08-12 11:15:11] TEST api_fetch_user ..... PASS
[2023-08-12 11:15:12] TEST api_create_user ..... FAIL
[2023-08-12 11:15:13] TEST api_delete_user ..... FAIL
[2023-08-12 11:15:14] TEST api_update_user ..... PASS
EOF

RUN chmod -R a+rX /home/user && \
    chmod 0777 /home/user/qa_logs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"