FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="chatgpt"
LABEL Description="Apptainer image for PostgreSQL EXPLAIN task with mocked Docker CLI and pytest installed."

# Install packages and pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directories
RUN mkdir -p /home/user/query_plans && \
    chmod 0777 /home/user/query_plans

# Create /usr/local/bin if not exists
RUN mkdir -p /usr/local/bin

# Mock Docker CLI
RUN cat << 'EOF' > /usr/local/bin/docker
#!/usr/bin/env bash
# Very small mock of the Docker CLI, sufficient for the automated tests.

subcommand="$1"
shift || true

case "$subcommand" in
    ps)
        # Return the container name when filtered by it.
        while [[ $# -gt 0 ]]; do
            if [[ "$1" == *"name=pg-optimize"* ]]; then
                echo "pg-optimize"
                exit 0
            fi
            shift
        done
        ;;
    inspect)
        # Always report the correct image.
        echo "postgres:15"
        exit 0
        ;;
    exec)
        # Skip potential flags (-it, etc.) and the container name.
        while [[ $# -gt 0 && "$1" == -* ]]; do shift; done
        shift   # container name (pg-optimize)

        # Skip until we meet 'psql'
        while [[ $# -gt 0 && "$1" != "psql" ]]; do shift; done
        if [[ "$1" == "psql" ]]; then
            shift
            # Look for -c / -Atc flag; the following token is the SQL.
            while [[ $# -gt 1 ]]; do
                case "$1" in
                    -c|-Atc)
                        sql="$2"
                        break
                        ;;
                esac
                shift
            done

            if [[ "$sql" == *"SELECT 1"* ]]; then
                echo "1"
                exit 0
            fi

            if [[ "$sql" == *"EXPLAIN"* ]]; then
                echo "QUERY PLAN"
                echo "-----------"
                echo "Seq Scan on orders  (cost=0.00..431.00 rows=21000 width=4)"
                exit 0
            fi
        fi
        ;;
    *)
        ;;
esac

exit 0
EOF

RUN chmod +x /usr/local/bin/docker

# Environment variables
ENV PATH=/usr/local/bin:$PATH

# Fix home directory permissions
RUN chmod 755 /home/user