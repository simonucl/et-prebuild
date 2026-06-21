FROM ubuntu:22.04

# Help text
# This Apptainer image contains the pre-seeded HTML page and the tools
# (Python 3 and pytest) required for the “re-scrape the HTML table” exercise.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/projects/scrape/input

RUN cat > /home/user/projects/scrape/input/page.html <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Quarterly Sales</title>
</head>
<body>
    <h1>Quarter 1 Sales</h1>

    <table id="sales">
        <thead>
            <tr><th>Region</th><th>Sales</th><th>Quarter</th></tr>
        </thead>
        <tbody>
            <tr><td>North</td><td>$12,400</td><td>Q1</td></tr>
            <tr><td>South</td><td>$11,300</td><td>Q1</td></tr>
            <tr><td>East</td><td>$10,900</td><td>Q1</td></tr>
            <tr><td>West</td><td>$9,800</td><td>Q1</td></tr>
        </tbody>
    </table>
</body>
</html>
EOF

RUN chmod 0644 /home/user/projects/scrape/input/page.html && \
    chmod 0755 /home/user || true && \
    chmod 0755 /home/user/projects /home/user/projects/scrape /home/user/projects/scrape/input || true

LABEL Author="task-preparer"
LABEL Description="Environment for HTML table re-scrape task"