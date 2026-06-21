FROM ubuntu:22.04

# Author: incident-log-prep

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/logs && \
    chmod 0777 /home/user

RUN cat > /home/user/logs/combined.log <<'EOF'
{"ts":"2023-10-12T13:58:44Z","level":"INFO","code":20000,"msg":"healthcheck ok"}
{"ts":"2023-10-12T14:00:02Z","level":"WARN","code":49999,"msg":"slow response detected"}
{"ts":"2023-10-12T14:01:19Z","level":"ERROR","code":50203,"msg":"upstream connection reset"}
{"ts":"2023-10-12T14:03:11Z","level":"ERROR","code":50203,"msg":"upstream connection reset"}
{"ts":"2023-10-12T14:04:23Z","level":"INFO","code":20000,"msg":"healthcheck ok"}
{"ts":"2023-10-12T14:07:05Z","level":"WARN","code":40001,"msg":"client aborted request"}
{"ts":"2023-10-12T14:10:42Z","level":"ERROR","code":50401,"msg":"gateway timeout"}
{"ts":"2023-10-12T14:12:06Z","level":"ERROR","code":50203,"msg":"upstream connection reset"}
{"ts":"2023-10-12T14:14:55Z","level":"WARN","code":49999,"msg":"slow response detected"}
{"ts":"2023-10-12T14:16:03Z","level":"WARN","code":49999,"msg":"slow response detected"}
{"ts":"2023-10-12T14:17:17Z","level":"ERROR","code":50401,"msg":"gateway timeout"}
{"ts":"2023-10-12T14:20:00Z","level":"INFO","code":20000,"msg":"healthcheck ok"}
{"ts":"2023-10-12T14:25:12Z","level":"ERROR","code":50401,"msg":"gateway timeout"}
{"ts":"2023-10-12T14:31:30Z","level":"WARN","code":40001,"msg":"client aborted request"}
{"ts":"2023-10-12T14:35:01Z","level":"INFO","code":20000,"msg":"healthcheck ok"}
EOF

RUN chmod 0644 /home/user/logs/combined.log && \
    chmod 0755 /home/user/logs && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8