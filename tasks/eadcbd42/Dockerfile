FROM ubuntu:22.04

# Labels
LABEL Author="TaskSetup"
LABEL Description="Container pre-populated with documentation data for status-report task; pytest installed."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create docs directory
RUN mkdir -p /home/user/docs

# Create outlines.csv
RUN cat > /home/user/docs/outlines.csv <<'EOF'
Section,Filename,Status
Introduction,intro.md,published
Installation,install.md,draft
Usage,usage.md,draft
API,api.md,published
FAQ,faq.md,draft
EOF

# Create topics.json
RUN cat > /home/user/docs/topics.json <<'EOF'
[
  { "filename": "intro.md",  "title": "Project Introduction" },
  { "filename": "install.md", "title": "Installing the Project" },
  { "filename": "usage.md",  "title": "How to Use" },
  { "filename": "api.md",    "title": "API Reference" },
  { "filename": "faq.md",    "title": "Frequently Asked Questions" }
]
EOF

# Ensure correct permissions
RUN chmod 755 /home/user/docs && \
    chmod 644 /home/user/docs/outlines.csv /home/user/docs/topics.json && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"