FROM ubuntu:22.04

# Help text from %help
# This Apptainer image contains the initial immutable state for the
# "function frequency" profiling task. It provides:
#   - /home/user/profiles/callstack.log (22 lines of sample data)
#   - pytest (pre-installed)
# Students are expected to create /home/user/profiles/function_frequency.log
# during their solve phase.

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/profiles && \
    chmod 0777 /home/user/profiles

RUN cat > /home/user/profiles/callstack.log << 'EOF'
malloc
free
malloc
memcpy
malloc
memcpy
free
read
write
read
malloc
free
memcpy
write
write
malloc
free
read
memset
memset
malloc
write
EOF

RUN chmod 0444 /home/user/profiles/callstack.log

RUN chmod 755 /home/user

LABEL Author="example@example.com"
LABEL Description="Container for profiling frequency task – provides initial data and pytest."