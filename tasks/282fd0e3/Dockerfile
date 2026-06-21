FROM ubuntu:22.04

# Help text from %help not provided

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest jsonschema

RUN groupadd -r user && useradd -m -r -g user user

RUN mkdir -p /home/user/ir_case_41

RUN cat > /home/user/ir_case_41/login_schema.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "additionalProperties": false,
  "required": ["timestamp", "username", "src_ip", "auth_result"],
  "properties": {
    "timestamp": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "username": { "type": "string" },
    "src_ip": {
      "type": "string",
      "pattern": "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\.|$)){4}$"
    },
    "auth_result": {
      "type": "string",
      "enum": ["SUCCESS", "FAILURE"]
    }
  }
}
EOF

RUN cat > /home/user/ir_case_41/login_events.json <<'EOF'
[
  {
    "timestamp": "2023-08-25T03:12:11Z",
    "username": "alice",
    "src_ip": "10.0.0.5",
    "auth_result": "SUCCESS"
  },
  {
    "timestamp": "2023-08-25T03:14:47Z",
    "username": "bob",
    "src_ip": "172.16.4.20",
    "auth_result": "FAILURE"
  },
  {
    "timestamp": "2023-08-25 03:15:00",
    "username": "charlie",
    "src_ip": "192.168.1.99",
    "auth_result": "SUCCESS"
  },
  {
    "timestamp": "2023-08-25T03:19:00Z",
    "user": "dave",
    "src_ip": "8.8.8.8",
    "auth_result": "FAILURE"
  },
  {
    "timestamp": "2023-08-25T03:20:00Z",
    "username": "eve",
    "src_ip": "not_an_ip",
    "auth_result": "SUCCESS"
  },
  {
    "timestamp": "2023-08-25T03:25:00Z",
    "username": "alice",
    "src_ip": "10.0.0.5",
    "auth_result": "SUCCESS",
    "session_id": "abcd1234"
  },
  {
    "timestamp": "2023-08-25T03:31:00Z",
    "username": "frank",
    "src_ip": "203.0.113.55",
    "auth_result": "FAILURE"
  },
  {
    "timestamp": "2023-08-25T03:37:00Z",
    "username": "bob",
    "src_ip": "172.16.4.20",
    "auth_result": "SUCCESS"
  }
]
EOF

RUN chown -R user:user /home/user && \
    chmod -R go-rwx /home/user/ir_case_41 && \
    chmod 755 /home/user

ENV PATH=/home/user/.local/bin:$PATH

CMD ["/bin/bash"]