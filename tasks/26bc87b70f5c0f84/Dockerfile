FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash python3 sqlite3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

RUN mkdir -p /home/user/support_lab/incoming /home/user/support_lab/output \
    && chown -R user:user /home/user/support_lab

RUN cat > /home/user/support_lab/incoming/tickets.jsonl <<'EOF'
{"ticket_id":"TCK-1001","account":" acme ","requester_email":"ops@acme.test","status":"Open","priority":"2","created_at":"2026-06-20T09:00:00-04:00","updated_at":"2026-06-20T15:45:00-04:00","tags":["API"," timeout ","API"],"subject":"API timeout after deploy"}
{"ticket_id":"TCK-1002","account":"beta","requester_email":"billing@beta.test","status":"resolved","priority":5,"created_at":"2026-06-21T10:15:00Z","updated_at":"2026-06-21T12:45:00Z","tags":["billing","invoice"],"subject":"Duplicate invoice generated"}
{"ticket_id":"TCK-1002","account":"beta","requester_email":"billing@beta.test","status":"resolved","priority":5,"created_at":"2026-06-21T10:15:00Z","updated_at":"2026-06-21T12:00:00Z","tags":["billing","stale"],"subject":"Stale duplicate invoice row"}
{"ticket_id":"TCK-1003","account":"cygnus","requester_email":"help@cygnus.test","status":"PENDING","priority":"3","created_at":"2026-06-22T08:00:00+02:00","updated_at":"2026-06-22T09:30:00+02:00","tags":["login","mfa"],"subject":"MFA code delayed"}
{"ticket_id":"TCK-1004","account":"delta","requester_email":"reports@delta.test","status":"Resolved","priority":1,"created_at":"2026-06-23T01:00:00Z","updated_at":"2026-06-24T01:00:00Z","tags":["export","csv"],"subject":"CSV export missing rows"}
{"ticket_id":"TCK-BAD1","account":"epsilon","requester_email":"not-an-email","status":"open","priority":2,"created_at":"2026-06-24T09:00:00Z","updated_at":"2026-06-24T09:05:00Z","tags":["bad"],"subject":"Bad requester"}
{"ticket_id":"TCK-BAD2","account":"zeta","requester_email":"ops@zeta.test","status":"escalated","priority":4,"created_at":"2026-06-24T10:00:00Z","updated_at":"2026-06-24T10:10:00Z","tags":["bad"],"subject":"Bad status"}
{"ticket_id":"TCK-1005","account":"orion","requester_email":"hooks@orion.test","status":"open","priority":4,"created_at":"2026-06-24T16:30:00Z","updated_at":"2026-06-24T17:05:00Z","tags":["webhook","retry"],"subject":"Webhook retry storm"}
EOF

RUN cat > /home/user/support_lab/incoming/messages.csv <<'EOF'
message_id,ticket_id,author,created_at,body
MSG-1,TCK-1001,customer,2026-06-20T13:05:00Z,"API times out on every request"
MSG-2,TCK-1001,agent,2026-06-20T13:17:00Z,"Rolling back the deploy and checking timeout traces"
MSG-3,TCK-1002,customer,2026-06-21T10:20:00Z,"Invoice was duplicated"
MSG-4,TCK-1002,agent,2026-06-21T11:00:00Z,"Removed duplicate invoice from billing queue"
MSG-5,TCK-1003,customer,2026-06-22T06:20:00Z,"MFA code arrives after it expires"
MSG-6,TCK-1003,agent,2026-06-22T07:10:00Z,"Adjusted SMS provider routing"
MSG-7,TCK-1004,system,2026-06-23T01:05:00Z,"Export job started"
MSG-8,TCK-1004,customer,2026-06-23T02:00:00Z,"CSV export is missing rows for region west"
MSG-9,TCK-1004,agent,2026-06-23T03:30:00Z,"Rebuilt export index and requeued CSV"
MSG-10,TCK-1005,customer,2026-06-24T16:31:00Z,"Webhook retry storm after 503 responses"
MSG-11,TCK-1005,agent,2026-06-24T16:50:00Z,"Disabled failing webhook endpoint"
MSG-12,TCK-9999,agent,2026-06-24T18:00:00Z,"Unknown ticket should be rejected"
MSG-13,TCK-1001,bot,2026-06-20T13:30:00Z,"Invalid author should be rejected"
EOF

RUN chown -R user:user /home/user/support_lab
USER user
