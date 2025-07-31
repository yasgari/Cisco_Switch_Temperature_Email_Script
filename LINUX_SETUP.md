# Linux/Ubuntu Hourly Scheduling Setup

## Quick Setup for Ubuntu/Linux

### 1. Open your crontab editor
```bash
crontab -e
```

### 2. Add this line to run every hour
```bash
0 * * * * cd /home/yourusername/cisco-temp-monitor && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

**Important:** Replace `/home/yourusername/cisco-temp-monitor` with your actual project path.

### 3. Find your project path
If you're not sure of your exact path, run this in your project directory:
```bash
pwd
```

### 4. Create log directory (if needed)
```bash
sudo mkdir -p /var/log
sudo touch /var/log/temp_monitor.log
sudo chmod 666 /var/log/temp_monitor.log
```

### 5. Verify your cron job
```bash
crontab -l
```

## Alternative Schedules

**Every hour during business hours (9 AM - 5 PM, weekdays):**
```bash
0 9-17 * * 1-5 cd /path/to/project && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

**Every 30 minutes:**
```bash
0,30 * * * * cd /path/to/project && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

**Every 2 hours:**
```bash
0 */2 * * * cd /path/to/project && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

## Testing Your Setup

### 1. Test manually first
```bash
cd /path/to/your/project
python3 checktemp_enhanced.py
```

### 2. Test the exact cron command
```bash
cd /path/to/your/project && python3 checktemp_enhanced.py >> /tmp/test.log 2>&1
cat /tmp/test.log
```

### 3. Check if cron is running
```bash
sudo systemctl status cron
```

## Monitoring Your Scheduled Runs

### View recent logs
```bash
tail -f /var/log/temp_monitor.log
```

### Check cron execution logs
```bash
grep CRON /var/log/syslog | tail -10
```

### View last 50 lines of logs
```bash
tail -50 /var/log/temp_monitor.log
```

## Troubleshooting

### Common Issues:

1. **Permission denied on log file:**
```bash
sudo chmod 666 /var/log/temp_monitor.log
```

2. **Python3 not found:**
```bash
which python3
# Use the full path in your cron job, e.g.:
# 0 * * * * cd /path/to/project && /usr/bin/python3 checktemp_enhanced.py
```

3. **Environment variables not loaded:**
Cron has a minimal environment. Make sure your `.env` file is in the project directory.

4. **Path issues:**
Always use absolute paths in cron jobs:
```bash
0 * * * * cd /home/yourusername/cisco-temp-monitor && /usr/bin/python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

## Quick Copy-Paste Setup

1. **Get your project path:**
```bash
cd your-project-directory
pwd
```

2. **Open cron editor:**
```bash
crontab -e
```

3. **Add this line (replace YOUR_PATH):**
```bash
0 * * * * cd YOUR_PATH && python3 checktemp_enhanced.py >> /var/log/temp_monitor.log 2>&1
```

4. **Save and exit** (Ctrl+X, then Y, then Enter if using nano)

5. **Create log file:**
```bash
sudo touch /var/log/temp_monitor.log
sudo chmod 666 /var/log/temp_monitor.log
```

That's it! Your script will now run every hour and send temperature reports automatically.