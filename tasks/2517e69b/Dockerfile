FROM ubuntu:22.04

# Help text from %help
# This container image provides the initial state required for the automated
# QA-summary task. It ships with:
#   • The exact raw log files under /home/user/test_results/raw_logs
#   • pytest installed for the grading harness
# All directories under /home/user/test_results are world-writable so an
# unprivileged agent can create the expected summary artefacts.

LABEL Author="Container prep for QA summary task"
LABEL Description="Includes initial raw logs and pytest for validation."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip locales && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8

RUN mkdir -p /home/user/test_results/raw_logs

RUN cat >/home/user/test_results/raw_logs/run1.log <<'EOF'
[2024-01-01 10:00:00] INFO Starting test suite
[2024-01-01 10:00:01] TESTCASE: login_functionality RESULT: PASS TIME: 1.2
[2024-01-01 10:00:02] TESTCASE: payment_gateway RESULT: FAIL TIME: 3.8
[2024-01-01 10:00:03] INFO Suite finished
EOF

RUN cat >/home/user/test_results/raw_logs/run2.log <<'EOF'
[2024-01-01 11:00:00] INFO Starting test suite
[2024-01-01 11:00:01] TESTCASE: search_functionality RESULT: PASS TIME: 0.9
[2024-01-01 11:00:02] TESTCASE: checkout_process RESULT: PASS TIME: 2.5
[2024-01-01 11:00:03] ERROR Unexpected timeout in payment_gateway
[2024-01-01 11:00:04] INFO Suite finished
EOF

RUN cat >/home/user/test_results/raw_logs/run3.log <<'EOF'
[2024-01-01 12:00:00] INFO Starting test suite
[2024-01-01 12:00:01] TESTCASE: user_profile RESULT: PASS TIME: 1.7
[2024-01-01 12:00:02] TESTCASE: password_reset RESULT: PASS TIME: 2.1
[2024-01-01 12:00:03] INFO Suite finished
EOF

RUN chmod -R 0777 /home/user/test_results

RUN mkdir -p /home/user && chmod 755 /home/user