FROM ubuntu:22.04

# Help text from %runscript
# Container for the inventory-service migration exercise.
# Run your commands as instructed in the task description.

LABEL Author="InventoryServicePrep"
LABEL Description="Sets up initial state for the inventory-service migration exercise."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip
RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/microservices/inventory-service

RUN cat > /home/user/microservices/inventory-service/config.json <<'EOF'
{
  "serviceName": "inventory-service",
  "port": 8080,
  "dbHost": "db.internal.old-cluster.local",
  "dbPort": 5432,
  "logLevel": "INFO"
}
EOF

RUN chmod -R a+rwX /home/user

CMD /bin/sh -c "echo 'Container for the inventory-service migration exercise.' && echo 'Run your commands as instructed in the task description.'"