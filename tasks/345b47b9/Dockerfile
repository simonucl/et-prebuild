FROM ubuntu:22.04

# Help / metadata extracted from %labels
LABEL Author="ChatGPT"
LABEL Description="Environment for UNIX permission auditing task"

ENV LANG=C
ENV LC_ALL=C

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 777 /home/user

RUN mkdir -p /home/user/web && \
    cat <<'EOF' > /home/user/web/targets.html
<!DOCTYPE html>
<html>
  <head><title>Permission Targets</title></head>
  <body>
    <h1>Files to Audit</h1>
    <ul>
      <li>/home/user/test_data/file_public.txt</li>
      <li>/home/user/test_data/file_secure.txt</li>
      <li>/home/user/test_data/exec.sh</li>
    </ul>
  </body>
</html>
EOF

RUN chmod 644 /home/user/web/targets.html

RUN mkdir -p /home/user/test_data && \
    echo "Public test file" > /home/user/test_data/file_public.txt && \
    chmod 644 /home/user/test_data/file_public.txt

RUN echo "Secure test file" > /home/user/test_data/file_secure.txt && \
    chmod 750 /home/user/test_data/file_secure.txt

RUN cat <<'EOF' > /home/user/test_data/exec.sh
#!/bin/bash
echo "Executable test file"
EOF

RUN chmod 755 /home/user/test_data/exec.sh

RUN rm -rf /home/user/audit