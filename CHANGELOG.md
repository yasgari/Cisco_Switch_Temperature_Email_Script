# Changelog

All notable changes to the Cisco Switch Temperature Monitor project will be documented in this file.

## [2.0.0] - 2025-07-30

### Added
- **Alert Detection System**: Automatically scans switch output for "warning" and "critical" conditions
- **Enhanced PDF Reports**: Alert summary section at top of PDF with red highlighting for problematic switches
- **Alert-Aware Email Notifications**: Modified email subjects and urgent body text when issues are detected
- **Intelligent Visual Highlighting**: Red text for alert lines in PDF reports
- **Comprehensive Logging**: Detailed logging system for troubleshooting and audit trails
- **Environment Variable Support**: Added .env file support for easier configuration management
- **Professional Documentation**: Complete GitHub repository setup with README, setup guides, and examples

### Enhanced
- **PDF Generation**: Improved formatting with custom styles for alerts and warnings
- **Email System**: Enhanced with conditional subject lines and alert-specific body content
- **Error Handling**: Better exception handling and user-friendly error messages
- **Configuration Management**: Flexible configuration through .env files or environment variables

### Technical Improvements
- Added `python-dotenv` support for environment variable management
- Enhanced PDF styling with ReportLab custom paragraph styles
- Improved hostname extraction from switch command output
- Better email attachment handling for both PDF and text files

## [1.0.0] - Initial Release

### Added
- Basic temperature monitoring functionality
- SSH connection to Cisco switches using Netmiko
- Excel file configuration for switch details
- Simple text file output generation
- Basic email sending capability
- PDF report generation using ReportLab

### Features
- Connect to multiple Cisco switches via SSH
- Execute temperature monitoring commands
- Generate timestamped output files
- Send email reports with attachments
- Professional PDF formatting for temperature readings