FROM ubuntu:22.04

# Ensure user-installed Python tools are found first
ENV PATH=/usr/local/bin:$PATH

# Author example
# Purpose "Container for single-command JSON summarization task"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output && \
    chmod 755 /home/user /home/user/output

RUN cat > /home/user/data/scan_results.json << 'EOF'
[
  {"id":"VULN-001","name":"Remote Code Execution","severity":"critical","cvss":9.8},
  {"id":"VULN-002","name":"SQL Injection","severity":"high","cvss":9.0},
  {"id":"VULN-003","name":"Directory Traversal","severity":"medium","cvss":6.5},
  {"id":"VULN-004","name":"Buffer Overflow","severity":"critical","cvss":9.1},
  {"id":"VULN-005","name":"Cross-Site Scripting","severity":"low","cvss":4.3}
]
EOF

RUN cat > /home/user/data/scan_schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id","name","severity","cvss"],
    "properties": {
      "id": {"type":"string"},
      "name": {"type":"string"},
      "severity": {"type":"string","enum":["critical","high","medium","low"]},
      "cvss": {"type":"number"}
    },
    "additionalProperties": false
  }
}
EOF