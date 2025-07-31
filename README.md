# Cisco Switch Temperature Monitor

An automated network monitoring system that checks temperature status on Cisco switches via SSH, generates professional PDF reports, and sends email alerts when warning or critical conditions are detected.

## Features

- **🌡️ Temperature Monitoring**: Automatically connects to multiple Cisco switches and executes temperature monitoring commands
- **📊 Professional PDF Reports**: Generates formatted PDF reports with temperature readings from all monitored switches
- **🚨 Intelligent Alert Detection**: Automatically detects and categorizes temperature conditions by severity
- **🎨 Color-Coded PDF Reports**: Yellow text for warnings, red text for critical/catastrophic conditions
- **📧 Smart Email Notifications**: Subject lines indicate severity level with appropriate urgency
- **⚠️ Alert Prioritization**: Critical alerts shown first at top of PDF reports for immediate attention
- **📝 Comprehensive Logging**: Detailed logging for troubleshooting and audit trails

## Screenshots

### Normal Temperature Report
- Clean PDF layout with all switch temperature readings
- Professional email notification with standard subject line

### Color-Coded Alert Detection
- **Critical Alerts**: Red text and headers, priority placement at top of PDF
- **Warning Alerts**: Yellow/orange text for warnings, secondary placement
- **Email Subject Lines**: 
  - Critical: "🚨 CRITICAL ALERT: Cisco switch device temperature update [timestamp] - Critical issues on [switch names]"
  - Warning: "⚠️ WARNING: Cisco switch device temperature update [timestamp] - Warnings on [switch names]"
- **Visual Hierarchy**: Critical problems highlighted in red throughout the detailed report

## Prerequisites

- Python 3.7 or higher
- Network access to target Cisco switches via SSH
- Valid SSH credentials for switch access
- SMTP server access for email functionality (Gmail, company email server, etc.)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yasgari/Cisco_Switch_Temperature_Email_Script.git
   cd Cisco_Switch_Temperature_Email_Script
   ```

2. **Install required packages**:
   ```bash
   pip3 install -r project_requirements.txt
   ```
   
   Or install packages individually:
   ```bash
   pip3 install netmiko pandas openpyxl reportlab python-dotenv
   ```

3. **Configure switch connections**:
   - Edit `switchFile.xlsx` with your actual switch details
   - Include: device_type, host, username, password, port, secret

4. **Set up email configuration**:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your email settings

## Configuration

### Switch Configuration File

The `switchFile.xlsx` file should contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| device_type | Cisco device type | cisco_ios |
| host | IP address or hostname | 192.168.1.10 |
| username | SSH username | admin |
| password | SSH password | yourpassword |
| port | SSH port (usually 22) | 22 |
| secret | Enable password (if required) | enablepass |

### Email Configuration

Create a `.env` file in the project root with your email settings:

```env
# SMTP Server Configuration (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# For Outlook/Office 365, use:
# SMTP_SERVER=smtp-mail.outlook.com
# SMTP_PORT=587

# Email Credentials
SENDER_EMAIL=monitoring@yourcompany.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=admin@yourcompany.com

# Multiple Recipients (comma-separated)
# RECIPIENT_EMAIL=admin@yourcompany.com,networkteam@yourcompany.com,manager@yourcompany.com

# Optional Settings
CLEANUP_FILES_AFTER_EMAIL=false
```

#### Email Provider Configurations

**Gmail Setup:**
1. Enable 2-factor authentication on your Google account
2. Generate an "App Password" in Google Account settings
3. Use the app password (not your regular password) in `SENDER_PASSWORD`
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-digit-app-password
```

**Outlook/Office 365 Setup:**
1. Enable "App passwords" in Microsoft Account security settings (if 2FA is enabled)
2. For corporate accounts, check with IT about authentication requirements
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your-email@outlook.com
SENDER_PASSWORD=your-password-or-app-password
```

**Corporate Exchange Server:**
Contact your IT department for specific settings:
```env
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587  # or 25, 465 depending on configuration
SENDER_EMAIL=your-email@yourcompany.com
SENDER_PASSWORD=your-domain-password
```

#### Multiple Recipients

The script supports sending emails to multiple recipients. Simply separate email addresses with commas in the `RECIPIENT_EMAIL` field:

```env
# Single recipient
RECIPIENT_EMAIL=admin@yourcompany.com

# Multiple recipients
RECIPIENT_EMAIL=admin@yourcompany.com,networkteam@yourcompany.com,manager@yourcompany.com
```

**Important notes:**
- All recipients will receive the same email with attachments
- Critical and warning alerts will be sent to all recipients
- Spaces around commas are automatically handled
- Ensure all email addresses are valid to avoid delivery failures

## Usage

### Basic Usage

Run the temperature monitoring script:
```bash
python3 checktemp_enhanced.py
```

The script will:
1. Read switch configurations from `switchFile.xlsx`
2. Connect to each switch via SSH
3. Execute temperature monitoring commands
4. Analyze output for warning/critical conditions
5. Generate PDF and text reports
6. Send email notifications with attachments

### Testing Without Real Switches

To test the alert detection and PDF generation features:
```bash
python3 test_alert_detection.py
```

This creates sample reports with simulated warning and critical conditions.

### Automated Scheduling

To run the script automatically every hour on Linux/Ubuntu systems, see the [Linux Setup Guide](LINUX_SETUP.md) for detailed instructions.

Quick setup:
```bash
# Open cron editor
crontab -e

# Add this line (replace with your actual project path):
0 * * * * cd /path/to/your/project && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

### Creating Sample Excel File

To generate a template Excel file with sample data:
```bash
python3 create_sample_excel.py
```

## Output Files

The script generates timestamped files:
- `device_output_YYYYMMDD_HHMMSS.txt` - Raw text output from all switches
- `device_temperature_report_YYYYMMDD_HHMMSS.pdf` - Professional PDF report

## Alert Detection

The system automatically scans switch output for:
- Lines containing "warning" (case-insensitive)
- Lines containing "critical" (case-insensitive)

When alerts are detected:
- **PDF Report**: Shows red warning banner at top with affected switch names
- **Email Subject**: Modified to include "🚨 ALERT" and affected switch names
- **Email Body**: Includes urgent attention notice and detailed alert information

## Troubleshooting

### Common Issues

**Connection Failures:**
```
TCP connection to device failed
```
- Verify switch IP addresses and SSH connectivity
- Check firewall rules and network access
- Confirm SSH is enabled on switches

**Excel File Errors:**
```
Excel file format cannot be determined
```
- Ensure `switchFile.xlsx` exists and is properly formatted
- Try recreating the file using `create_sample_excel.py`

**Email Authentication Errors:**
```
Username and Password not accepted
```
- For Gmail: Use app password, not regular password
- Verify SMTP server settings in `.env` file
- Check with IT department for company email requirements

### Logging

The script provides detailed logging output. Check the console for:
- Connection status to each switch
- Temperature alert detection results
- PDF generation status
- Email sending results

## Scheduling

### Windows Task Scheduler
Create a scheduled task to run the script automatically.

### Linux/Mac Cron
Add to crontab for regular execution:
```bash
# Run every hour
0 * * * * /path/to/python3 /path/to/checktemp_enhanced.py

# Run daily at 6 AM
0 6 * * * /path/to/python3 /path/to/checktemp_enhanced.py
```

## Security Considerations

- Store credentials securely (use `.env` file, not hardcoded)
- Limit SSH access to monitoring systems only
- Use dedicated service accounts for switch access
- Consider using SSH keys instead of passwords where possible
- Regularly rotate passwords and app passwords

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs for detailed error information
3. Open an issue in the GitHub repository

## Acknowledgments

- Built with [Netmiko](https://github.com/ktbyers/netmiko) for network device automation
- PDF generation powered by [ReportLab](https://www.reportlab.com/)
- Excel file handling via [Pandas](https://pandas.pydata.org/) and [OpenPyXL](https://openpyxl.readthedocs.io/)
