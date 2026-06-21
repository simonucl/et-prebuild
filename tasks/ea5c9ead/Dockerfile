FROM ubuntu:22.04

# Labels
LABEL Author="sandbox"
LABEL Description="Mock backup-service container for reliability engineering exercise"

# Environment
ENV LC_ALL=C.UTF-8

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

# Mock backup-service implementation
RUN cat > /home/user/mock_backup_api.py <<'PY'
#!/usr/bin/env python3
"""
Light-weight HTTP server that mimics the internal "backup-service".

Endpoints and exact JSON payloads:

  GET  /status           -> {"service":"backup","status":"OK"}
  GET  /last-backup      -> {"last_backup":"2023-08-28T02:14:26Z"}
  GET  /list             -> [{"id":1,"timestamp":"2023-08-26T01:00:00Z"}, ...]
  POST /trigger-backup   -> {"triggered":true}
  GET  /download/2       -> {"id":2,"data":"SGVsbG8="}

The byte lengths of the bodies are fixed and verified by the grader, so
DO NOT modify them.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re

# Exact response bodies (no whitespace changes!)
RESPONSES = {
    "/status":          '{"service":"backup","status":"OK"}',
    "/last-backup":     '{"last_backup":"2023-08-28T02:14:26Z"}',
    "/list":            '[{"id":1,"timestamp":"2023-08-26T01:00:00Z"},'
                        '{"id":2,"timestamp":"2023-08-27T01:00:00Z"},'
                        '{"id":3,"timestamp":"2023-08-28T02:14:26Z"}]',
    "/trigger-backup":  '{"triggered":true}',
    "/download/2":      '{"id":2,"data":"SGVsbG8="}',
}

DOWNLOAD_RE = re.compile(r"^/download/(\d+)$")


class BackupRequestHandler(BaseHTTPRequestHandler):
    # Silence the default logging to avoid cluttering the console
    def log_message(self, *_args, **_kwargs):
        pass

    def _send_json(self, body: str, status_code: int = 200):
        body_bytes = body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    # ---------------------------
    # GET
    # ---------------------------
    def do_GET(self):
        if self.path in RESPONSES and self.path != "/trigger-backup":
            self._send_json(RESPONSES[self.path])
            return

        # Handle /download/<id> (only id=2 is valid)
        m = DOWNLOAD_RE.match(self.path)
        if m and m.group(1) == "2":
            self._send_json(RESPONSES["/download/2"])
            return

        # Anything else is 404
        self.send_error(404, "Not Found")

    # ---------------------------
    # POST
    # ---------------------------
    def do_POST(self):
        # We accept /trigger-backup with any (or no) JSON body
        if self.path == "/trigger-backup":
            # Read and ignore incoming body if present
            length = int(self.headers.get("Content-Length", 0))
            if length:
                self.rfile.read(length)
            self._send_json(RESPONSES["/trigger-backup"])
            return

        self.send_error(404, "Not Found")


def main():
    server_address = ("0.0.0.0", 9090)
    httpd = HTTPServer(server_address, BackupRequestHandler)
    print("Mock backup-service listening on 0.0.0.0:9090")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
PY

# Set permissions
RUN chmod 755 /home/user/mock_backup_api.py && \
    chown -R root:root /home/user && \
    chmod 755 /home/user

# Help information (as comments):
# This container supplies:
#   • /home/user/mock_backup_api.py – a small HTTP service that the
#     student must start themselves on port 9090.
#   • pytest – used by the automated grader.
#
# No result directories or files are pre-created; the student must
# create everything under /home/user/backup_test during the task.