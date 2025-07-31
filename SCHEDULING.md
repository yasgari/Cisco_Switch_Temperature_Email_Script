# Automated Scheduling Guide

This guide explains how to set up the temperature monitoring script to run automatically every hour on different operating systems.

## Linux/macOS - Using Cron

### 1. Open the cron editor
```bash
crontab -e
```

### 2. Add the hourly job
Add this line to run the script every hour:
```bash
0 * * * * cd /path/to/your/project && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

**Important:** Replace `/path/to/your/project` with the actual path to your project folder.

### 3. Alternative: Run every hour during business hours (9 AM - 5 PM)
```bash
0 9-17 * * 1-5 cd /path/to/your/project && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

### 4. Verify the cron job
```bash
crontab -l
```

### Cron Format Explanation
```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, Sunday=0 or 7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

## Windows - Using Task Scheduler

### Method 1: Using Command Line (schtasks)

Open Command Prompt as Administrator and run:

```cmd
schtasks /create /tn "Temperature Monitor" /tr "python3 C:\path\to\your\project\checktemp_enhanced.py" /sc hourly /st 09:00
```

**Replace** `C:\path\to\your\project` with your actual project path.

### Method 2: Using Task Scheduler GUI

1. **Open Task Scheduler:**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task:**
   - Click "Create Basic Task" in the right panel
   - Name: "Temperature Monitor"
   - Description: "Hourly Cisco switch temperature monitoring"

3. **Set Trigger:**
   - Choose "Daily"
   - Set start date and time (e.g., today at 9:00 AM)
   - Check "Repeat task every: 1 hours"
   - Check "for a duration of: 1 day"

4. **Set Action:**
   - Choose "Start a program"
   - Program: `python3` (or full path: `C:\Python3\python.exe`)
   - Arguments: `checktemp_enhanced.py`
   - Start in: `C:\path\to\your\project`

5. **Finish and Test:**
   - Click "Finish"
   - Right-click the task and select "Run" to test

## macOS - Using launchd (Alternative to cron)

### 1. Create a plist file
Create file: `~/Library/LaunchAgents/com.yourcompany.tempmonitor.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourcompany.tempmonitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/project/checktemp_enhanced.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/your/project</string>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/tempmonitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/tempmonitor.error.log</string>
</dict>
</plist>
```

### 2. Load the job
```bash
launchctl load ~/Library/LaunchAgents/com.yourcompany.tempmonitor.plist
```

### 3. Start the job
```bash
launchctl start com.yourcompany.tempmonitor
```

## Server Environments

### Using systemd (Linux servers)

1. **Create service file:** `/etc/systemd/system/temp-monitor.service`
```ini
[Unit]
Description=Cisco Temperature Monitor
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python3 checktemp_enhanced.py
StandardOutput=journal
StandardError=journal
```

2. **Create timer file:** `/etc/systemd/system/temp-monitor.timer`
```ini
[Unit]
Description=Run Cisco Temperature Monitor every hour
Requires=temp-monitor.service

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

3. **Enable and start:**
```bash
sudo systemctl enable temp-monitor.timer
sudo systemctl start temp-monitor.timer
```

### Docker with Cron

Create a `Dockerfile` for containerized deployment:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Add cron job
RUN echo "0 * * * * cd /app && python3 checktemp_enhanced.py" | crontab -

CMD ["cron", "-f"]
```

## Logging and Monitoring

### Enable detailed logging
Add this to your `.env` file:
```env
# Logging configuration
LOG_LEVEL=INFO
LOG_FILE=/var/log/cisco_temp_monitor.log
```

### Monitor the scheduled runs
```bash
# View recent runs (Linux/macOS)
tail -f /var/log/temp_monitor.log

# Check cron logs (Linux)
grep CRON /var/log/syslog

# View systemd timer status (Linux)
systemctl status temp-monitor.timer
```

## Troubleshooting

### Common Issues

1. **Path Problems:**
   - Use absolute paths in scheduled tasks
   - Verify Python3 is in the system PATH
   - Test the exact command manually first

2. **Permission Issues:**
   - Ensure the user has read/write access to the project directory
   - Check log file permissions
   - Verify network access for SSH connections

3. **Environment Variables:**
   - Cron jobs have minimal environment variables
   - Use absolute paths for .env file if needed
   - Test with: `env | grep PATH` in your cron job

### Testing Your Schedule

Before setting up the full schedule, test the command manually:
```bash
cd /path/to/your/project
python3 checktemp_enhanced.py
```

Then test with the exact command you'll use in the scheduler:
```bash
cd /path/to/your/project && python3 checktemp_enhanced.py >> /tmp/test.log 2>&1
```

## Best Practices

1. **Log Everything:** Always redirect output to log files for debugging
2. **Use Absolute Paths:** Avoid relative paths in scheduled tasks
3. **Test First:** Run the exact command manually before scheduling
4. **Monitor Initially:** Check logs frequently when first setting up
5. **Handle Failures:** Consider adding error notifications or retry logic
6. **Resource Usage:** Monitor system resources during scheduled runs

## Security Considerations

- Store credentials securely in the `.env` file with proper permissions (`chmod 600 .env`)
- Consider using SSH keys instead of passwords for switch access
- Rotate passwords regularly
- Monitor log files for unauthorized access attempts
- Consider running the script as a dedicated user with minimal privileges