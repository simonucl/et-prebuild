FROM ubuntu:22.04

# Help / labels converted as comments
# Maintainer: ChatGPT
# Description: Environment for FinOps analyst task – mock API data pre-seeded, pytest installed.

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/finops/mock_api && \
    mkdir -p /home/user/finops/responses

RUN cat <<'EOF' > /home/user/finops/mock_api/cost-data.json
{
  "accountId": "123456789012",
  "currency": "USD",
  "totalMonthlyCost": 1423.55,
  "services": [
    { "name": "AmazonEC2", "monthlyCost": 823.10 },
    { "name": "AmazonS3", "monthlyCost": 211.22 },
    { "name": "AmazonRDS", "monthlyCost": 389.23 }
  ]
}
EOF

RUN cat <<'EOF' > /home/user/finops/mock_api/rightsizing-suggestions.json
{
  "generatedAt": "2023-10-01T00:00:00Z",
  "suggestions": [
    { "name": "i-02468ec2", "monthlySavings": 120.35 },
    { "name": "i-13579ec2", "monthlySavings": 98.99 },
    { "name": "db-42rds", "monthlySavings": 45.10 }
  ]
}
EOF

RUN chmod -R 777 /home/user

CMD ["/bin/bash"]