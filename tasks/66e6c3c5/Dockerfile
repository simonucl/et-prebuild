FROM ubuntu:22.04

# Basic tooling and Python
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest beautifulsoup4 lxml

# Ensure the standard non-privileged user directory exists
RUN useradd -m -u 1000 -s /bin/bash user || true

# Prepare the offline web-mirror exactly as described in the spec
RUN mkdir -p /home/user/webmirror

# targets.lst – each line ends with a newline character
RUN cat > /home/user/webmirror/targets.lst <<'EOF'
site1.html
site2.html
site3.html
EOF

# site1.html
RUN cat > /home/user/webmirror/site1.html <<'EOF'
<!DOCTYPE html>
<html>
  <head>
    <title>Site One</title>
    <script src="http://insecure.example.com/evil.js"></script>
    <script>
      // harmless comment
      console.log("hello");
    </script>
  </head>
  <body>
    <h1>Welcome to Site 1</h1>
    <script>
      eval("alert('xss')");   // use of eval, vulnerability
    </script>
  </body>
</html>
EOF

# site2.html
RUN cat > /home/user/webmirror/site2.html <<'EOF'
<!DOCTYPE html>
<html>
  <head>
    <title>Site Two</title>
    <script src="https://secure.example.com/safe.js"></script>
  </head>
  <body>
    <h1>All good here</h1>
  </body>
</html>
EOF

# site3.html
RUN cat > /home/user/webmirror/site3.html <<'EOF'
<!DOCTYPE html>
<html>
  <head>
    <title>Site Three</title>
    <script src="http://cdn.example.com/lib.js"></script>
    <script src="http://bad.example.com/tracker.js"></script>
  </head>
  <body>
    <h1>Tracking central</h1>
    <!-- no eval here -->
  </body>
</html>
EOF

# Permissions: readable by the runtime user, no vulnscan dir yet
RUN chmod -R a+rX /home/user/webmirror

# Ensure files/directories inside /home/user are owned by UID 1000
RUN chown -R 1000:1000 /home/user || true

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Labels
LABEL Author="PenTest Task Setup"
LABEL Description="Offline web-mirror penetration-testing exercise – initial state"

# Help information (as comments):
# This container image sets up the initial filesystem state for the
# "offline mirror penetration-testing" exercise.
#
# Key locations inside the image:
#
#   /home/user/webmirror/           – Contains the three HTML files
#                                     and targets.lst enumerating them.
#
# The learner's solution script must create:
#
#   /home/user/vulnscan/vulnerability_report.json
#
# and finally print its absolute path.