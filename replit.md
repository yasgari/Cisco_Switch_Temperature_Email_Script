# Switch Temperature Monitoring System

## Overview

This repository contains a Python-based network monitoring system designed to check temperature status on network switches via SSH. The system reads switch connection details from an Excel file, connects to each switch using Netmiko, executes temperature monitoring commands, and generates reports in both text and PDF formats with optional email distribution.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a straightforward procedural architecture with two main components:

1. **Core Script (`attached_assets/checktemp_1753906779886.py`)**: Basic temperature monitoring functionality
2. **Enhanced Script (`checktemp_enhanced.py`)**: Extended version with PDF reporting and email capabilities

The system operates as a batch processing tool that:
- Reads configuration from Excel files
- Executes commands on network devices via SSH
- Processes and formats output
- Generates reports and notifications

## Key Components

### Network Communication
- **Netmiko Library**: Handles SSH connections to network switches
- **Connection Management**: Automatic connection establishment and cleanup
- **Command Execution**: Remote command execution with output capture

### Data Processing
- **Pandas Integration**: Excel file reading and data manipulation
- **DataFrame Operations**: Converting spreadsheet data to usable Python dictionaries
- **Output Aggregation**: Collecting and formatting command results

### Reporting System
- **Text Output**: Basic console and string-based reporting
- **PDF Generation**: ReportLab-based PDF document creation with custom formatting
- **Email Distribution**: SMTP-based email sending with PDF attachments

### Configuration Management
- **Excel-based Configuration**: Switch details stored in `switchFile.xlsx`
- **Command Lists**: Configurable commands for execution on devices

## Data Flow

1. **Initialization**: Load switch configuration from Excel file
2. **Connection Loop**: Iterate through each switch in the configuration
3. **Command Execution**: Connect via SSH and execute temperature monitoring commands
4. **Data Collection**: Aggregate output from all switches with timestamps and hostnames
5. **Report Generation**: Create formatted reports (text and PDF)
6. **Distribution**: Optional email delivery of reports

## External Dependencies

### Core Libraries
- `netmiko`: Network device SSH automation
- `pandas`: Data manipulation and Excel file handling
- `datetime`/`time`: Timestamp management

### Enhanced Features
- `reportlab`: PDF document generation
- `smtplib`: Email sending functionality
- `email.mime.*`: Email formatting and attachment handling
- `logging`: Application logging and debugging

### System Dependencies
- Excel file (`switchFile.xlsx`) containing switch connection parameters
- Network connectivity to target switches
- SMTP server access for email functionality

## Deployment Strategy

The application is designed for:

### Local Execution
- Direct Python script execution on administrator workstations
- Manual or scheduled execution via cron/task scheduler
- Standalone operation with minimal setup requirements

### Configuration Requirements
- Excel file with switch connection details (host, username, password, device_type)
- Network access to target switches via SSH (typically port 22)
- Optional SMTP server configuration for email reports

### Output Management
- Local file system storage for generated reports
- Timestamp-based file naming for historical tracking
- Configurable output directories

### Error Handling
- Connection timeout management
- Exception handling for network failures
- Logging for troubleshooting and audit trails

The system prioritizes simplicity and reliability, making it suitable for network administrators who need regular temperature monitoring without complex infrastructure requirements.