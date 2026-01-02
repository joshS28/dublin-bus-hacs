# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please do the following:

1. **Do NOT** open a public issue
2. Email the maintainer directly (check GitHub profile for contact)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Considerations

### API Key Storage

- API keys are stored in Home Assistant's configuration
- Keys are encrypted at rest by Home Assistant
- Never commit API keys to the repository
- Use environment variables for testing

### Data Privacy

- This integration only communicates with the NTA API
- No user data is collected or transmitted elsewhere
- All data is processed locally in Home Assistant

### Network Security

- All API calls use HTTPS
- API key is sent in headers, not URL parameters
- No sensitive data is logged

## Best Practices for Users

1. Keep Home Assistant updated
2. Use strong passwords for Home Assistant
3. Enable two-factor authentication
4. Restrict network access to Home Assistant
5. Regularly review API key usage in NTA portal
6. Revoke and regenerate API keys if compromised

## Dependency Security

We monitor dependencies for known vulnerabilities:
- `gtfs-realtime-bindings`
- `protobuf`
- `requests`

Updates are released promptly when security issues are discovered.
