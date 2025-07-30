# Quick Setup Guide

## Step-by-Step Installation

### 1. Prerequisites
- Python 3.7 or higher installed
- Network access to your Cisco switches
- Email account for sending reports

### 2. Download and Install

```bash
# Clone or download the repository
git clone https://github.com/yourusername/cisco-temperature-monitor.git
cd cisco-temperature-monitor

# Install required packages
pip install -r project_requirements.txt
```

### 3. Configure Switches

Edit `switchFile.xlsx` with your switch information:

| device_type | host | username | password | port | secret |
|-------------|------|----------|----------|------|--------|
| cisco_ios | 192.168.1.10 | admin | yourpass | 22 | enablepass |
| cisco_ios | 192.168.1.11 | admin | yourpass | 22 | enablepass |

### 4. Setup Email

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your email settings
nano .env  # or use your preferred editor
```

Example `.env` content:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=monitoring@yourcompany.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=admin@yourcompany.com
```

### 5. Test Run

```bash
# Test with sample data (no switches required)
python test_alert_detection.py

# Run with your actual switches
python checktemp_enhanced.py
```

## Gmail Setup

1. Go to Google Account settings
2. Enable 2-factor authentication
3. Generate an App Password:
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the 16-character password
4. Use this app password in your `.env` file

## Troubleshooting

**Can't connect to switches?**
- Check IP addresses and SSH connectivity
- Verify credentials in Excel file
- Ensure SSH is enabled on switches

**Email not working?**
- For Gmail: Use app password, not regular password
- Check SMTP server settings
- Test with a simple email first

**Excel file errors?**
- Run `python create_sample_excel.py` to recreate the file
- Ensure all required columns are present

## Next Steps

- Set up scheduled execution (Task Scheduler/cron)
- Customize alert detection rules if needed
- Add more switches to monitor
- Configure backup email recipients