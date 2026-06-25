FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash python3 zip unzip ca-certificates \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user \
  && mkdir -p /home/user/book_src/chapters /home/user/book_src/assets /home/user/book_src/notes /home/user/handoff \
  && printf '%s\n' '{"name":"field-runbook","version":"2.0.0","identifier":"urn:uuid:3b1e14b9-8b51-43dd-9c4a-7630e0d2b30f","language":"en","title":"Field Runbook","creator":"Acme Operations"}' > /home/user/book_src/book.json \
  && printf '%s\n' '# Introduction' '' 'This runbook is used by the Acme field team before a maintenance window.' '' '- Verify the relay is reachable.' '- Record the ticket number.' > /home/user/book_src/chapters/intro.md \
  && printf '%s\n' '# Operating Checklist' '' 'Follow this checklist in order.' '' '1. Put the relay into drain mode.' '2. Confirm the queue depth is zero.' '3. Resume traffic and capture the health probe.' > /home/user/book_src/chapters/ops.md \
  && printf '%s\n' 'body { font-family: sans-serif; line-height: 1.45; }' 'nav ol { padding-left: 1.5em; }' 'code { font-family: monospace; }' > /home/user/book_src/assets/book.css \
  && printf '%s\n' '<svg xmlns="http://www.w3.org/2000/svg" width="160" height="48" viewBox="0 0 160 48">' '  <rect width="160" height="48" fill="#f5f5f5"/>' '  <text x="16" y="30" font-family="sans-serif" font-size="18">Acme Ops</text>' '</svg>' > /home/user/book_src/assets/logo.svg \
  && printf '%s\n' 'These notes are drafting-only material and must not be packaged.' > /home/user/book_src/notes/draft.txt \
  && chown -R user:user /home/user/book_src /home/user/handoff
