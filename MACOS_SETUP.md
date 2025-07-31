# macOS Setup Guide

## Architecture Compatibility Issue Fix

If you're getting an architecture error like this on Apple Silicon Macs (M1/M2/M3):
```
ImportError: dlopen(..._cffi_backend.cpython-39-darwin.so, 0x0002): tried: '...' (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64e' or 'arm64'))
```

This happens when Python packages were compiled for Intel x86_64 instead of ARM64.

## Solution Options

### Option 1: Reinstall with ARM64 Packages (Recommended)

1. **Uninstall existing packages:**
```bash
pip3 uninstall netmiko pandas openpyxl reportlab python-dotenv cryptography paramiko cffi -y
```

2. **Clear pip cache:**
```bash
pip3 cache purge
```

3. **Reinstall with ARM64 compatibility:**
```bash
pip3 install --no-cache-dir --force-reinstall netmiko pandas openpyxl reportlab python-dotenv
```

### Option 2: Use Homebrew Python (Recommended for Apple Silicon)

1. **Install Homebrew (if not installed):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install Python via Homebrew:**
```bash
brew install python@3.11
```

3. **Use Homebrew Python:**
```bash
/opt/homebrew/bin/python3 -m pip install netmiko pandas openpyxl reportlab python-dotenv
```

4. **Run script with Homebrew Python:**
```bash
/opt/homebrew/bin/python3 checktemp_enhanced.py
```

### Option 3: Create Virtual Environment with Correct Architecture

1. **Create virtual environment:**
```bash
python3 -m venv cisco_temp_monitor
source cisco_temp_monitor/bin/activate
```

2. **Install packages in virtual environment:**
```bash
pip install netmiko pandas openpyxl reportlab python-dotenv
```

3. **Run script in virtual environment:**
```bash
python checktemp_enhanced.py
```

### Option 4: Use pyenv for Python Version Management

1. **Install pyenv:**
```bash
brew install pyenv
```

2. **Install Python 3.11:**
```bash
pyenv install 3.11.9
pyenv global 3.11.9
```

3. **Restart terminal and install packages:**
```bash
pip install netmiko pandas openpyxl reportlab python-dotenv
```

## Verification

After fixing the architecture issue, verify the installation:

```bash
python3 -c "import netmiko; print('✓ Netmiko imported successfully')"
python3 -c "import pandas; print('✓ Pandas imported successfully')"
python3 -c "import openpyxl; print('✓ OpenPyXL imported successfully')"
python3 -c "import reportlab; print('✓ ReportLab imported successfully')"
```

## Quick Test

Run the test script to verify everything works:
```bash
python3 test_normal_temps.py
```

You should see:
- Text file created successfully
- PDF generated successfully
- No import errors

## Troubleshooting

### If you still get import errors:

1. **Check Python architecture:**
```bash
python3 -c "import platform; print(platform.machine())"
```
Should show `arm64` on Apple Silicon Macs.

2. **Check installed packages architecture:**
```bash
pip3 show cryptography | grep Location
file /path/to/cryptography
```

3. **Force reinstall problematic packages:**
```bash
pip3 uninstall cryptography cffi -y
pip3 install --no-cache-dir cryptography cffi
```

### If Homebrew Python doesn't work:

1. **Add Homebrew to PATH:**
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

2. **Verify Homebrew Python:**
```bash
which python3
# Should show: /opt/homebrew/bin/python3
```

## Notes

- Apple Silicon Macs (M1/M2/M3) use ARM64 architecture
- Intel Macs use x86_64 architecture
- Mixed architecture packages cause import errors
- Virtual environments help isolate package installations
- Homebrew provides ARM64-native packages for Apple Silicon

## Excel File Setup

Don't forget to:
1. Copy `switchFile.xlsx` to your project directory
2. Update switch IP addresses, usernames, and passwords
3. Copy `.env.example` to `.env` and configure email settings

For complete setup instructions, see `README.md`.