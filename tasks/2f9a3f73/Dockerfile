FROM ubuntu:22.04

# Help:
# This image provides the initial environment for the
# "active users" CSV/JSON processing exercise.
# Key pre-created artefact:
#   /home/user/project/data/users.csv
# pytest is installed so that the supplied test suites can be run.

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/data

RUN cat << 'EOF' > /home/user/project/data/users.csv
id,name,email,status
1,John Doe,john@example.com,active
2,Jane Smith,jane@sample.com,inactive
3,Bob Lee,bob@domain.com,active
4,Alice Kay,alice@website.org,pending
EOF

RUN chmod -R a+rwX /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8

CMD echo "Container for the 'active users' exercise. Execute your commands inside an interactive shell." && exec /bin/bash "$@"