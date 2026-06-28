FROM ubuntu:22.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

LABEL Description="terminal-rsi env: semver upgrade-plan generator (prerelease precedence + yanked filtering + byte-exact JSON/log)"

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create the unprivileged working account layout.
RUN useradd -m -u 1000 -s /bin/bash user && \
    mkdir -p /home/user/registry && \
    chmod 755 /home/user /home/user/registry

# Stage the registry of package metadata files. Each file is named
#   <package>@<version>.meta
# and contains key=value lines (size_bytes / published / yanked).
# NOTE: this generator stages ONLY the starting state, never the expected answer.
RUN python3 - <<'PYEOF'
import os
REG="/home/user/registry"
DATA={
 "atlas":[("1.8.0",10485760,1640995200,False),("1.9.0",12582912,1656633600,False),("1.10.0",13631488,1672531200,True)],
 "borealis":[("0.9.0",5242880,1643673600,False),("0.10.0",5500000,1659312000,False),("0.10.1",5600000,1661990400,False)],
 "cobalt":[("3.0.0-alpha",100,1646092800,False),("3.0.0-alpha.1",200,1646179200,False),("3.0.0-beta",300,1648771200,False),("3.0.0",4000000,1651363200,False),("3.0.1",4100000,1654041600,False)],
 "delta":[("5.2.0-rc.2",700,1665619200,False),("5.2.0-rc.10",800,1665705600,False),("5.2.0",9000000,1668297600,False)],
 "mosaic":[("1.0.0",2000000,1633046400,False),("1.2.0",2500000,1638316800,False),("2.0.0-rc.1",900,1675209600,False),("2.0.0-rc.2",1000,1675296000,False)],
}
for pkg,vers in DATA.items():
    for v,size,pub,yanked in vers:
        with open(os.path.join(REG,f"{pkg}@{v}.meta"),"w") as f:
            f.write(f"size_bytes={size}\n")
            f.write(f"published={pub}\n")
            f.write(f"yanked={'true' if yanked else 'false'}\n")
PYEOF

RUN chown -R user:user /home/user/registry && chmod 644 /home/user/registry/*.meta

USER user
WORKDIR /home/user
