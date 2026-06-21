FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/experiments/opt_solver && \
    chmod -R 0777 /home/user

# Create solver_run.log via heredoc
RUN cat > /home/user/experiments/opt_solver/solver_run.log <<'EOF'
iteration,objective,elapsed_sec
1,12.34,0.5
2,7.89,1.0
3,5.67,1.5
4,4.56,2.0
5,4.12,2.5
final,4.12,2.5
EOF

# Ensure the log file is writable
RUN chmod 666 /home/user/experiments/opt_solver/solver_run.log

# Environment variables
ENV PYTHONIOENCODING=UTF-8

# Match environment chmod behavior
RUN chmod 755 /home/user

# Default run command
CMD ["bash"]