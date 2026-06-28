FROM ubuntu:24.04

WORKDIR /home/user

RUN mkdir -p /home/user/ledger/source/configs \
    /home/user/ledger/source/data/transactions \
    /home/user/ledger/source/logs \
    /home/user/ledger/source/tmp

RUN printf '%s\n' \
    '# Ledger Export' \
    '' \
    'Quarterly ledger extract for offline archival testing.' \
    > /home/user/ledger/source/README.md

RUN printf '%s\n' \
    '[ledger]' \
    'currency=USD' \
    'retention_days=30' \
    'mode=batch' \
    > /home/user/ledger/source/configs/app.ini

RUN printf '%s\n' \
    'account_id,name,status' \
    '1001,Cash,active' \
    '2001,Accounts Receivable,active' \
    '3001,Revenue,active' \
    > /home/user/ledger/source/data/accounts.csv

RUN printf '%s\n' \
    'txn_id,account_id,amount' \
    'JAN-001,1001,1250.00' \
    'JAN-002,3001,-1250.00' \
    > /home/user/ledger/source/data/transactions/jan.csv

RUN printf 'runtime noise\n' > /home/user/ledger/source/logs/runtime.log && \
    printf 'cache noise\n' > /home/user/ledger/source/tmp/cache.bin && \
    chmod -R u+rwX,go+rX /home/user/ledger && \
    find /home/user/ledger/source -type f -exec touch -d '2026-01-15 00:00:00 UTC' {} + && \
    find /home/user/ledger/source -type d -exec touch -d '2026-01-15 00:00:00 UTC' {} +

CMD ["bash"]
