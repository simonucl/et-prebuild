FROM ubuntu:22.04

# Install Python tooling (pytest must be available for the grader)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up the documentation project's initial fixture
RUN mkdir -p /home/user/docs/chapter1 /home/user/docs/chapter2

# chapter1/introduction.md
RUN cat > /home/user/docs/chapter1/introduction.md <<'EOF'
# Introduction
Overview of the project.
TODO: add more detail about scope
Additional background text.
TODO - revise later
EOF

# chapter1/setup.md
RUN cat > /home/user/docs/chapter1/setup.md <<'EOF'
# Setup
Prerequisites
Build instructions.
TODO : include installation steps
EOF

# chapter2/advanced-topics.md
RUN cat > /home/user/docs/chapter2/advanced-topics.md <<'EOF'
# Advanced Topics
TODO: add performance tips
TODO - add case studies
Completed first draft.
EOF

# Permissions: allow the unprivileged runtime user to create files
# (e.g., todo_summary.log) inside /home/user/docs
RUN chmod 777 /home/user/docs && \
    chmod -R a+r /home/user/docs && \
    chmod 755 /home/user

# Ensure pip-installed executables are found
ENV PATH="/usr/local/bin:${PATH}"