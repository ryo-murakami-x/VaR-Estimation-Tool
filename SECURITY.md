# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the VaR Estimation Tool, please email
security@example.com with the following information:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

**Please do not open a public issue for security vulnerabilities.**

We take security seriously and will:
1. Confirm receipt of your report within 48 hours
2. Assess the vulnerability
3. Work on a fix
4. Release a security update
5. Credit you if desired (with your permission)

## Security Best Practices for Users

- Keep your Python installation and dependencies up to date
- Use a virtual environment to isolate dependencies
- Be cautious when loading data from untrusted sources
- Review code before running it on sensitive systems
- Report suspicious behavior to the maintainers

## Supported Versions

| Version | Status | Support Ends |
|---------|--------|-------------|
| 1.0.x   | ✅ Supported | TBD |

## Security Updates

Security updates will be released as soon as possible after a vulnerability is identified and patched.

Users are encouraged to stay updated by:
- Watching the GitHub repository for releases
- Subscribing to security advisories
- Keeping dependencies updated: `pip install --upgrade -r requirements.txt`

## Dependencies Security

This project uses the following dependencies:
- pandas: Financial data manipulation
- numpy: Numerical computations
- matplotlib: Data visualization

All dependencies are regularly monitored for security vulnerabilities.
