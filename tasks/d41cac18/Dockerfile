FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/raw_data && \
    chmod 755 /home/user && \
    chmod 755 /home/user/raw_data

# Create test_cases.list (colon ":" separated, with trailing newline)
RUN cat >/home/user/raw_data/test_cases.list <<'EOF'
TC001:UserLogin:env1
TC002:UserLogout:env1
TC003:PurchaseItem:env2
TC004:CancelOrder:env2
TC005:ApplyCoupon:env3
EOF

# Create statuses.log (comma "," separated, with trailing newline)
RUN cat >/home/user/raw_data/statuses.log <<'EOF'
TC001,PASS
TC002,FAIL
TC003,PASS
TC004,SKIP
TC005,FAIL
EOF

# Create durations.csv (semicolon ";" separated, with trailing newline)
RUN cat >/home/user/raw_data/durations.csv <<'EOF'
TC001;1023
TC002;980
TC003;2150
TC004;1500
TC005;1175
EOF

RUN chmod 644 /home/user/raw_data/*