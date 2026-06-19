# Security Policy

## Reporting a Vulnerability

We take the security of BQ Assistant seriously. If you believe you have found a security vulnerability, please report it to us by emailing security@bq.ai.

## Security Features

- **Encryption**: All sensitive data is encrypted using AES-256-GCM.
- **Authentication**: JWT-based authentication with short-lived access tokens.
- **Rate Limiting**: Protection against brute-force and DDoS attacks.
- **Input Sanitization**: Prevention of XSS and SQL injection.
- **CSRF Protection**: Protection against cross-site request forgery.
- **Audit Logging**: Comprehensive logging of security-related events.

## Secure Development Lifecycle

We follow a secure development lifecycle, including:
- Automated security testing in CI/CD.
- Regular dependency audits.
- Code reviews focused on security.
