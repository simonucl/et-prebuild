FROM ubuntu:22.04

# Basic build tooling and Python + pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the tests
RUN mkdir -p /home/user/observability/logs && \
    chmod -R a+rwx /home/user

# Provide the raw application event log
# – exactly 60 lines
# – event-code frequencies must match the task description
RUN cat <<'EOF' > /home/user/observability/logs/app_events.log
2023-08-01T10:00:01Z EVT_DATA_SYNC user=alice
2023-08-01T10:00:02Z EVT_LOGIN user=bob
2023-08-01T10:00:03Z EVT_DATA_SYNC user=charlie
2023-08-01T10:00:04Z EVT_LOGOUT user=dave
2023-08-01T10:00:05Z EVT_DATA_SYNC user=erin
2023-08-01T10:00:06Z EVT_TIMEOUT user=frank
2023-08-01T10:00:07Z EVT_ERROR user=alice
2023-08-01T10:00:08Z EVT_LOGIN user=bob
2023-08-01T10:00:09Z EVT_DATA_SYNC user=charlie
2023-08-01T10:00:10Z EVT_LOGOUT user=dave
2023-08-01T10:00:11Z EVT_DATA_SYNC user=erin
2023-08-01T10:00:12Z EVT_TIMEOUT user=frank
2023-08-01T10:00:13Z EVT_ERROR user=alice
2023-08-01T10:00:14Z EVT_LOGIN user=bob
2023-08-01T10:00:15Z EVT_DATA_SYNC user=charlie
2023-08-01T10:00:16Z EVT_LOGOUT user=dave
2023-08-01T10:00:17Z EVT_DATA_SYNC user=erin
2023-08-01T10:00:18Z EVT_TIMEOUT user=frank
2023-08-01T10:00:19Z EVT_ERROR user=alice
2023-08-01T10:00:20Z EVT_LOGIN user=bob
2023-08-01T10:00:21Z EVT_DATA_SYNC user=charlie
2023-08-01T10:00:22Z EVT_LOGOUT user=dave
2023-08-01T10:00:23Z EVT_DATA_SYNC user=erin
2023-08-01T10:00:24Z EVT_ERROR user=frank
2023-08-01T10:00:25Z EVT_LOGIN user=alice
2023-08-01T10:00:26Z EVT_DATA_SYNC user=bob
2023-08-01T10:00:27Z EVT_LOGOUT user=charlie
2023-08-01T10:00:28Z EVT_DATA_SYNC user=dave
2023-08-01T10:00:29Z EVT_TIMEOUT user=erin
2023-08-01T10:00:30Z EVT_ERROR user=frank
2023-08-01T10:00:31Z EVT_LOGIN user=alice
2023-08-01T10:00:32Z EVT_DATA_SYNC user=bob
2023-08-01T10:00:33Z EVT_LOGOUT user=charlie
2023-08-01T10:00:34Z EVT_DATA_SYNC user=dave
2023-08-01T10:00:35Z EVT_ERROR user=erin
2023-08-01T10:00:36Z EVT_LOGIN user=frank
2023-08-01T10:00:37Z EVT_DATA_SYNC user=alice
2023-08-01T10:00:38Z EVT_LOGOUT user=bob
2023-08-01T10:00:39Z EVT_DATA_SYNC user=charlie
2023-08-01T10:00:40Z EVT_TIMEOUT user=dave
2023-08-01T10:00:41Z EVT_ERROR user=erin
2023-08-01T10:00:42Z EVT_LOGIN user=frank
2023-08-01T10:00:43Z EVT_DATA_SYNC user=alice
2023-08-01T10:00:44Z EVT_LOGOUT user=bob
2023-08-01T10:00:45Z EVT_DATA_SYNC user=charlie
2023-08-01T10:00:46Z EVT_ERROR user=dave
2023-08-01T10:00:47Z EVT_LOGIN user=erin
2023-08-01T10:00:48Z EVT_DATA_SYNC user=frank
2023-08-01T10:00:49Z EVT_LOGOUT user=alice
2023-08-01T10:00:50Z EVT_LOGIN user=bob
2023-08-01T10:00:51Z EVT_TIMEOUT user=charlie
2023-08-01T10:00:52Z EVT_ERROR user=dave
2023-08-01T10:00:53Z EVT_LOGIN user=erin
2023-08-01T10:00:54Z EVT_DATA_SYNC user=frank
2023-08-01T10:00:55Z EVT_LOGOUT user=alice
2023-08-01T10:00:56Z EVT_LOGIN user=bob
2023-08-01T10:00:57Z EVT_LOGIN user=charlie
2023-08-01T10:00:58Z EVT_LOGIN user=dave
2023-08-01T10:00:59Z EVT_DATA_SYNC user=erin
2023-08-01T10:01:00Z EVT_LOGOUT user=frank
EOF

RUN chmod 755 /home/user

# Author: Observability-Task-Builder
# Description: Container image prepared for the Event Code Frequency Report exercise.