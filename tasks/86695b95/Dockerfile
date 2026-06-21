# Author: QA-AI Assistant
# Description: Container for the “awk & sed QA-reports” assignment – initial state only.
# Help:
# This container provides the initial filesystem state for the “awk & sed QA-reports”
# assignment, along with Python and pytest for automated evaluation.

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/qa_reports

RUN cat <<'EOF' > /home/user/qa_reports/run1.log
2023-07-01 10:00:01 [INFO] TESTCASE Login PASS
2023-07-01 10:00:05 [INFO] TESTCASE Logout PASS
2023-07-01 10:00:07 [INFO] TESTCASE ProfileUpdate FAIL
2023-07-01 10:00:10 [INFO] Environment cleanup complete
EOF

RUN cat <<'EOF' > /home/user/qa_reports/run2.log
2023-07-01 11:00:01 [INFO] TESTCASE Signup PASS
2023-07-01 11:00:05 [INFO] TESTCASE PasswordReset FAIL
2023-07-01 11:00:07 [INFO] TESTCASE TwoFactorAuth FAIL
2023-07-01 11:00:10 [INFO] Environment cleanup complete
EOF

RUN cat <<'EOF' > /home/user/qa_reports/run3.log
2023-07-01 12:00:01 [INFO] TESTCASE Search PASS
2023-07-01 12:00:05 [INFO] TESTCASE AddToCart PASS
2023-07-01 12:00:07 [INFO] TESTCASE Checkout PASS
2023-07-01 12:00:10 [INFO] Environment cleanup complete
EOF

RUN chmod 777 /home/user/qa_reports && \
    chmod 666 /home/user/qa_reports/*.log && \
    chmod 755 /home/user