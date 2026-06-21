FROM ubuntu:22.04

# Author: SecurityExerciseSetup
# Description: Environment for credential-rotation log analysis task
# Help:
# This image provides the starting environment for the credential-rotation log analysis exercise.
# The required raw log file is located at:
#     /home/user/security/logs/2024-credential-rotation.log
# Pytest is pre-installed for automated grading.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/security/logs

RUN cat <<'EOF' > /home/user/security/logs/2024-credential-rotation.log
2024-06-11T14:22:01Z [INFO] Service 'api-gateway' credential rotation successful
2024-06-11T14:25:47Z [WARNING] Service 'auth-service' credential expired, rotation required
2024-06-11T14:26:02Z [ERROR] Service 'auth-service' credential expired, failed automatic rotation
2024-06-11T14:30:12Z [INFO] User 'alice' authenticated to 'git-server'
2024-06-11T14:35:55Z [INFO] Service 'db-backend' credential rotation scheduled
2024-06-11T14:36:07Z [ERROR] Service 'db-backend' credential expired, rotation halted
2024-06-11T14:40:11Z [WARNING] Service 'billing-service' credential expired, awaiting rotation
2024-06-11T14:45:23Z [INFO] Service 'message-queue' credential rotation successful
2024-06-11T14:47:58Z [ERROR] Service 'message-queue' credential expired, failed automatic rotation
2024-06-11T14:48:12Z [INFO] User 'svc_analytics' obtained temporary token
2024-06-11T14:49:42Z [INFO] User 'svc_billing' token refresh completed
2024-06-11T14:50:21Z [WARNING] User 'svc_marketing' failed token refresh attempt
2024-06-11T14:52:07Z [INFO] Background job 'rotate-keys' finished
2024-06-11T14:53:17Z [INFO] Service 'search-service' credential rotation successful
2024-06-11T14:54:20Z [WARNING] Service 'search-service' credential expired, rotation required
2024-06-11T14:55:09Z [INFO] User 'bob' logged out
2024-06-11T14:56:30Z [INFO] User 'svc_billing' credential renewed
2024-06-11T14:57:41Z [ERROR] Service 'auth-service' credential expired, rotation attempt failed again
2024-06-11T15:01:26Z [INFO] CRON 'cleanup-temp' completed
2024-06-11T15:02:57Z [INFO] User 'svc_reporting' authenticated
EOF

RUN chmod -R 0777 /home/user/security

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PYTHONIOENCODING=utf8

CMD echo "Container for credential-rotation task. Open a shell to begin work:" && exec /bin/bash "$@"