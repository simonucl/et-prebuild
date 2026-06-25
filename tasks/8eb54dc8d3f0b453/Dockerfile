FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/pkg-src/package/bin /app/pkg-src/package/src/Acme/Console /app/pkg-src/package/tests /app/repo/dist \
  && cat > /app/pkg-src/package/composer.json <<'EOF'
{
  "name": "acme/edge-probe",
  "description": "Edge probe helpers for internal diagnostics",
  "type": "library",
  "license": "MIT",
  "autoload": {
    "psr-4": {
      "Acme\\EdgeProbe\\": "src/Acme/"
    }
  },
  "bin": [
    "bin/edge-probe"
  ],
  "require": {
    "php": ">=8.1"
  }
}
EOF
RUN cat > /app/pkg-src/package/LICENSE <<'EOF'
MIT License

Copyright (c) 2026 Acme Edge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction.
EOF
RUN cat > /app/pkg-src/package/README.md <<'EOF'
# acme/edge-probe

Small diagnostic helpers used by the edge operations team.
EOF
RUN cat > /app/pkg-src/package/bin/edge-probe <<'EOF'
#!/usr/bin/env php
<?php
echo "edge-probe ready\n";
EOF
RUN chmod 755 /app/pkg-src/package/bin/edge-probe
RUN cat > /app/pkg-src/package/src/Acme/EdgeProbe.php <<'EOF'
<?php
namespace Acme\EdgeProbe;

final class EdgeProbe
{
    public static function status(): string
    {
        return 'ready';
    }
}
EOF
RUN cat > /app/pkg-src/package/src/Acme/Console/ProbeCommand.php <<'EOF'
<?php
namespace Acme\EdgeProbe\Console;

use Acme\EdgeProbe\EdgeProbe;

final class ProbeCommand
{
    public function __invoke(): string
    {
        return EdgeProbe::status();
    }
}
EOF
RUN cat > /app/pkg-src/package/tests/ProbeTest.php <<'EOF'
<?php
// Development-only fixture. Do not ship in the dist archive.
EOF
RUN cat > /app/pkg-src/package/README.md~ <<'EOF'
draft copy
EOF
RUN cat > /app/repo/packages.json <<'EOF'
{"packages":[]}
EOF
RUN printf 'placeholder\n' > /app/repo/dist/acme-edge-probe-2.3.1.zip
