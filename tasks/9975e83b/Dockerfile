FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user
RUN useradd -m -u 1000 user

# Create starter .bashrc using heredoc
RUN cat > /home/user/.bashrc <<'EOF'
# ~/.bashrc - initial content for compliance exercise
echo "Interactive Bash shell initialized."
EOF

# Ensure newline and correct ownership
RUN echo >> /home/user/.bashrc && chown user:user /home/user/.bashrc

# Apply environment‑style command
RUN chmod 755 /home/user

# Run script equivalent
CMD ["sh", "-c", "echo 'Container for HISTTIMEFORMAT compliance task ready.'"]