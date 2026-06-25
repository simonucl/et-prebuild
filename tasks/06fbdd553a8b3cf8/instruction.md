# Repair the Offline Edge PKI Bundle

You are preparing a small offline certificate bundle under `/home/user/pki-lab`.
The root CA and two certificate signing requests are already present:

- `/home/user/pki-lab/root/certs/root.cert.pem`
- `/home/user/pki-lab/root/private/root.key.pem`
- `/home/user/pki-lab/incoming/edge-api.csr.pem`
- `/home/user/pki-lab/incoming/old-edge-agent.csr.pem`

Create an intermediate CA and release bundle without using the network.

Required end state:

1. Create these files:
   - `/home/user/pki-lab/intermediate/private/intermediate.key.pem`
   - `/home/user/pki-lab/out/intermediate.cert.pem`
   - `/home/user/pki-lab/out/chain.pem`
   - `/home/user/pki-lab/out/certs/edge-api.cert.pem`
   - `/home/user/pki-lab/out/certs/old-edge-agent.cert.pem`
   - `/home/user/pki-lab/out/crl/intermediate.crl.pem`
   - `/home/user/pki-lab/out/manifest.json`
2. The intermediate private key must be an RSA 3072-bit key with mode `0600`.
3. The intermediate certificate must be signed by the root CA and must be a CA certificate with:
   - subject `C=US, O=Acme Edge Labs, OU=Issuing, CN=Acme Edge Issuing CA`
   - critical `basicConstraints = CA:TRUE, pathlen:0`
   - critical `keyUsage = Certificate Sign, CRL Sign`
4. `chain.pem` must contain the intermediate certificate followed by the root certificate, in PEM format.
5. Sign `edge-api.csr.pem` as a server certificate using the intermediate CA:
   - RSA public key from the CSR
   - subject from the CSR
   - SANs: `DNS:edge-api.internal`, `DNS:edge-api.service.consul`, `IP:10.42.0.15`
   - critical key usage for digital signature and key encipherment
   - extended key usage for TLS Web Server Authentication
   - not a CA certificate
6. Sign `old-edge-agent.csr.pem` as a client certificate using the intermediate CA:
   - subject from the CSR
   - SAN `URI:spiffe://edge.local/agent/old-edge-agent-17`
   - critical key usage for digital signature
   - extended key usage for TLS Web Client Authentication
   - not a CA certificate
7. Revoke the old-edge-agent certificate with the intermediate CA and publish a PEM CRL at `/home/user/pki-lab/out/crl/intermediate.crl.pem`.
8. `manifest.json` must be minified JSON with exactly one trailing newline and this key order:

   ```json
   {"bundle":"edge-pki","issuer":"Acme Edge Issuing CA","server_cert":"certs/edge-api.cert.pem","revoked":["certs/old-edge-agent.cert.pem"],"crl":"crl/intermediate.crl.pem","sha256":{"intermediate.cert.pem":"<hex>","chain.pem":"<hex>","certs/edge-api.cert.pem":"<hex>","certs/old-edge-agent.cert.pem":"<hex>","crl/intermediate.crl.pem":"<hex>"}}
   ```

   The SHA-256 values must be computed from the final file bytes at those relative paths under `/home/user/pki-lab/out`.

Do not replace the certificates with placeholder text. The files must validate with OpenSSL offline.
