# Windows Hourly Scheduling Setup

## Quick Setup for Windows

### Method 1: Command Line (Recommended)

**Step 1: Open Command Prompt as Administrator**
- Press `Win + X` and select "Command Prompt (Admin)" or "PowerShell (Admin)"

**Step 2: Create the scheduled task**
```cmd
schtasks /create /tn "Cisco Temperature Monitor" /tr "python C:\path\to\your\project\checktemp_enhanced.py" /sc hourly /st 09:00
```

**Important:** Replace `C:\path\to\your\project` with your actual project path.

**Step 3: Verify the task was created**
```cmd
schtasks /query /tn "Cisco Temperature Monitor"
```

### Method 2: Task Scheduler GUI

**Step 1: Open Task Scheduler**
- Press `Win + R`, type `taskschd.msc`, press Enter
- Or search "Task Scheduler" in Start menu

**Step 2: Create Basic Task**
- Click "Create Basic Task..." in the right panel
- **Name:** `Cisco Temperature Monitor`
- **Description:** `Hourly network switch temperature monitoring`
- Click "Next"

**Step 3: Set Trigger**
- Select "Daily"
- Click "Next"
- Set **Start date:** Today's date
- Set **Start time:** `09:00:00` (or preferred start time)
- Check "Repeat task every: `1 hours`"
- Check "for a duration of: `1 day`"
- Click "Next"

**Step 4: Set Action**
- Select "Start a program"
- Click "Next"
- **Program/script:** `python` (or full path: `C:\Python3\python.exe`)
- **Add arguments:** `checktemp_enhanced.py`
- **Start in:** `C:\path\to\your\project`
- Click "Next"

**Step 5: Finish**
- Review settings
- Check "Open the Properties dialog for this task when I click Finish"
- Click "Finish"

**Step 6: Advanced Settings (Optional)**
- In Properties dialog, go to "Settings" tab
- Check "Run task as soon as possible after a scheduled start is missed"
- Check "If the task fails, restart every: `1 minute`" and set attempts to `3`
- Click "OK"

### Method 3: PowerShell Script

Create a PowerShell script to set up the task:

**Step 1: Create setup script**
Save this as `setup_scheduler.ps1`:

```powershell
# PowerShell script to create hourly temperature monitoring task
$TaskName = "Cisco Temperature Monitor"
$ScriptPath = "C:\path\to\your\project\checktemp_enhanced.py"  # UPDATE THIS PATH
$PythonPath = "python"  # or full path like "C:\Python3\python.exe"
$LogPath = "C:\temp\cisco_monitor.log"

# Create trigger for hourly execution
$Trigger = New-ScheduledTaskTrigger -Daily -At 9AM -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 1)

# Create action to run Python script
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory (Split-Path $ScriptPath)

# Create task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Settings $Settings -Description "Hourly Cisco switch temperature monitoring"

Write-Host "Task '$TaskName' created successfully!"
Write-Host "Check Task Scheduler to verify the task is active."
```

**Step 2: Run the setup script**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_scheduler.ps1
```

## Find Your Python Path

If you're not sure where Python is installed:

**Command Prompt:**
```cmd
where python
```

**PowerShell:**
```powershell
Get-Command python
```

**Common Python locations:**
- `C:\Python3\python.exe`
- `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe`
- `C:\Program Files\Python311\python.exe`

## Find Your Project Path

**In Command Prompt/PowerShell:**
```cmd
cd your-project-directory
cd
```

**In File Explorer:**
- Navigate to your project folder
- Click in the address bar to see the full path
- Copy the path (e.g., `C:\Users\YourName\Documents\cisco-temp-monitor`)

## Managing the Scheduled Task

### View task status
```cmd
schtasks /query /tn "Cisco Temperature Monitor" /fo LIST
```

### Run task manually (for testing)
```cmd
schtasks /run /tn "Cisco Temperature Monitor"
```

### Delete the task
```cmd
schtasks /delete /tn "Cisco Temperature Monitor" /f
```

### Modify schedule to run every 2 hours
```cmd
schtasks /change /tn "Cisco Temperature Monitor" /ri 120
```

### Disable the task
```cmd
schtasks /change /tn "Cisco Temperature Monitor" /disable
```

### Enable the task
```cmd
schtasks /change /tn "Cisco Temperature Monitor" /enable
```

## Monitoring and Logs

### Check task history
1. Open Task Scheduler
2. Navigate to "Task Scheduler Library"
3. Find "Cisco Temperature Monitor"
4. Click on "History" tab

### Enable task history (if disabled)
1. In Task Scheduler, click "Enable All Tasks History" in the Actions panel
2. Refresh the view

### View Windows Event Logs
```cmd
# View task scheduler events
eventvwr.msc
# Navigate to: Windows Logs > System
# Filter by Event ID: 106 (Task started), 102 (Task completed)
```

### Create log file for script output
Modify your task action to include logging:

**Program/script:** `cmd`
**Arguments:** `/c python C:\path\to\project\checktemp_enhanced.py >> C:\temp\cisco_monitor.log 2>&1`
**Start in:** `C:\path\to\project`

## Troubleshooting

### Common Issues:

**1. Task runs but script fails:**
- Check that Python is in the system PATH
- Use full path to python.exe: `C:\Python3\python.exe`
- Verify the working directory is set correctly

**2. Permission denied:**
- Run Command Prompt as Administrator when creating tasks
- Ensure the user account has permissions to run scheduled tasks

**3. Script can't find files:**
- Use absolute paths in the task configuration
- Set the "Start in" directory to your project folder

**4. Task doesn't run at scheduled time:**
- Check if computer is sleeping/hibernating
- In Task Scheduler Properties > Settings, check "Wake the computer to run this task"

**5. Python not found:**
```cmd
# Install Python from Microsoft Store or python.org
# Add Python to PATH during installation
```

### Test Your Setup

**1. Test the script manually:**
```cmd
cd C:\path\to\your\project
python checktemp_enhanced.py
```

**2. Test the exact task command:**
```cmd
cd C:\path\to\your\project && python checktemp_enhanced.py
```

**3. Run the scheduled task manually:**
```cmd
schtasks /run /tn "Cisco Temperature Monitor"
```

## Security Considerations

- Store your `.env` file in a secure location with appropriate permissions
- Consider using Windows credential manager for sensitive information
- Run the task with a dedicated service account if in a corporate environment
- Regularly update passwords and review task permissions

## Alternative Schedules

**Every 30 minutes:**
```cmd
schtasks /create /tn "Cisco Temperature Monitor" /tr "python C:\path\to\project\checktemp_enhanced.py" /sc minute /mo 30
```

**Business hours only (9 AM - 5 PM):**
```cmd
schtasks /create /tn "Cisco Temperature Monitor" /tr "python C:\path\to\project\checktemp_enhanced.py" /sc hourly /st 09:00 /et 17:00
```

**Weekdays only:**
```cmd
schtasks /create /tn "Cisco Temperature Monitor" /tr "python C:\path\to\project\checktemp_enhanced.py" /sc weekly /d MON,TUE,WED,THU,FRI /st 09:00
```