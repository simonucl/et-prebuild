FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    coreutils \
    python3 \
    unzip \
    zip \
  && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p /app/nuget-src/lib/net8.0 /app/nuget-src/buildTransitive /app/nuget-feed/v3/flatcontainer/acme.edgerules/1.4.0 /app/nuget-feed/v3/registration/acme.edgerules; \
  printf 'ACME-EDGE-RULES IL STUB\nversion=1.4.0\ncommit=8f3d2ac91b7e\n' > /app/nuget-src/lib/net8.0/Acme.EdgeRules.dll; \
  printf '<Project>\n  <PropertyGroup>\n    <AcmeEdgeRulesEnabled>true</AcmeEdgeRulesEnabled>\n  </PropertyGroup>\n</Project>\n' > /app/nuget-src/buildTransitive/Acme.EdgeRules.props; \
  printf '# Acme.EdgeRules\n\nOffline edge routing rule helpers for Acme gateways.\n' > /app/nuget-src/README.md; \
  printf 'Copyright (c) Acme Corp.\nReleased under the MIT license.\n' > /app/nuget-src/LICENSE.txt; \
  printf '<package><metadata><id>Acme.EdgeRules</id><version>0.0.0-broken</version></metadata></package>\n' > /app/nuget-src/Acme.EdgeRules.nuspec.template; \
  printf 'not a zip archive\n' > /app/nuget-feed/v3/flatcontainer/acme.edgerules/1.4.0/acme.edgerules.1.4.0.nupkg; \
  printf '{"versions":["0.9.0"]}\n' > /app/nuget-feed/v3/flatcontainer/acme.edgerules/index.json; \
  printf '{"broken":true}\n' > /app/nuget-feed/v3/index.json; \
  printf '{"items":[]}\n' > /app/nuget-feed/v3/registration/acme.edgerules/index.json
