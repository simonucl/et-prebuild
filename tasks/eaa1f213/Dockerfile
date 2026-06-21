FROM ubuntu:22.04

# Labels
LABEL Author="qa-preparer"
LABEL Description="Starter image for QA frequency-count exercise (pytest pre-seeded)"

# Update package index and install Python tooling
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the verification test-suite
RUN pip3 install --no-cache-dir pytest

# Create required directory tree (except the 'logs' dir which must be absent initially)
RUN mkdir -p /home/user/qa_env/test_results

# Seed data file: /home/user/qa_env/test_results/raw_results.txt
RUN cat > /home/user/qa_env/test_results/raw_results.txt <<'EOF'
auth PASS
auth PASS
auth FAIL
payment PASS
payment PASS
payment PASS
payment FAIL
search PASS
search FAIL
search FAIL
search FAIL
report PASS
report PASS
report PASS
report PASS
EOF

# Permissions: Allow unprivileged container users to create new files
RUN chmod -R a+rwX /home/user/qa_env && \
    chmod 755 /home/user

# Environment
ENV HOME=/home/user

WORKDIR /home/user

CMD ["/bin/bash", "-c", "echo 'Container for the Sort & uniq frequency counting for QA test results exercise.' && echo 'Open a shell with: docker exec -it <container> /bin/bash' && exec /bin/bash"]