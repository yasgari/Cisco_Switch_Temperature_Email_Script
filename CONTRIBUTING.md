# Contributing to Cisco Switch Temperature Monitor

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or request features
- Include detailed information about your environment and steps to reproduce issues
- For security issues, please email maintainers directly rather than creating public issues

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes**:
   ```bash
   python test_alert_detection.py  # Test basic functionality
   python checktemp_enhanced.py    # Test with your switches (if available)
   ```
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
6. **Push and create a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/cisco-temperature-monitor.git
cd cisco-temperature-monitor

# Install dependencies
pip install -r project_requirements.txt

# Copy configuration template
cp .env.example .env
# Edit .env with your test settings

# Set up test switches in switchFile.xlsx
```

### Code Standards

- Follow PEP 8 Python style guidelines
- Add docstrings to new functions
- Include error handling for network operations
- Add logging statements for important operations
- Test with various switch configurations when possible

### Testing

- Run existing tests before submitting changes
- Add tests for new features when applicable
- Test with different switch models and configurations
- Verify email functionality with various SMTP servers

### Areas for Contribution

#### High Priority
- Support for additional switch models (Arista, Juniper, etc.)
- Enhanced alert detection rules and thresholds
- Web dashboard for monitoring multiple locations
- Database storage for historical temperature data

#### Medium Priority
- SNMP monitoring support as alternative to SSH
- Slack/Teams notification integration
- Custom email templates
- Configuration validation and setup wizard

#### Low Priority
- Docker containerization
- REST API for external integrations
- Mobile app notifications
- Advanced reporting and analytics

### Code Review Process

1. All submissions require review before merging
2. Reviewers will check for:
   - Code quality and style
   - Security considerations
   - Testing coverage
   - Documentation updates
3. Address feedback promptly
4. Squash commits if requested

### Security Considerations

- Never commit credentials or secrets
- Use environment variables for configuration
- Validate all user inputs
- Follow secure coding practices for network operations
- Consider impact of changes on credential handling

### Documentation

- Update README.md for new features
- Add examples for new functionality
- Update CHANGELOG.md with your changes
- Include inline comments for complex logic

## Questions?

- Open an issue for general questions
- Check existing issues and pull requests first
- Be respectful and constructive in all interactions

Thank you for contributing!