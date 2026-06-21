FROM ubuntu:22.04

# Author: Automated Build
# Description: Minimal repo API environment with pytest installed
# Help:
# This container image provides the starting point for the binary repository assignment.
# It already contains:
#   • /home/user/repo_api.py – the tiny HTTP JSON API service
#   • /home/user/repo_state/ – initial state with two artefacts
# Pytest and curl are installed. Nothing is listening on port 9123 yet; the student will start the service during the exercise.

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

RUN mkdir -p /home/user/repo_state && \
    mkdir -p /home/user/repo-tests/logs && \
    chmod 777 /home/user/repo_state && \
    chmod 777 /home/user/repo-tests && \
    chmod 777 /home/user/repo-tests/logs

RUN cat >/home/user/repo_state/artifacts.json <<'EOF'
["artifact-alpha", "artifact-beta"]
EOF

RUN chmod 666 /home/user/repo_state/artifacts.json

RUN cat >/home/user/repo_api.py <<'PYEOF'
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

STATE_PATH = "/home/user/repo_state/artifacts.json"

class RepoHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/v1/artifacts":
            with open(STATE_PATH) as fp:
                artifacts = json.load(fp)
            self._send_json(artifacts)
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/v1/artifacts":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                name = data["name"]
            except Exception:
                self.send_error(400, "Bad JSON")
                return
            with open(STATE_PATH) as fp:
                artifacts = json.load(fp)
            if name not in artifacts:
                artifacts.append(name)
            with open(STATE_PATH, "w") as fp:
                json.dump(artifacts, fp)
            self._send_json({"status": "stored"})
        else:
            self.send_error(404, "Not Found")

def main():
    os.makedirs("/home/user/repo_state", exist_ok=True)
    if not os.path.isfile(STATE_PATH):
        with open(STATE_PATH, "w") as fp:
            json.dump(["artifact-alpha", "artifact-beta"], fp)
    server = HTTPServer(("0.0.0.0", 9123), RepoHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
PYEOF

RUN chmod 755 /home/user/repo_api.py