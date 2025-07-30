#!/usr/bin/env python3
"""
Script to create a sample Excel file for switch configuration
This creates switchFile.xlsx with the proper structure
"""

import pandas as pd

# Sample switch data - replace with your actual switch information
switch_data = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.1.10',
        'username': 'admin',
        'password': 'password123',
        'port': 22,
        'secret': 'enable123'
    },
    {
        'device_type': 'cisco_ios', 
        'host': '192.168.1.11',
        'username': 'admin',
        'password': 'password123',
        'port': 22,
        'secret': 'enable123'
    },
    {
        'device_type': 'cisco_ios',
        'host': '10.0.0.5',
        'username': 'netadmin',
        'password': 'secure456',
        'port': 22,
        'secret': 'enable456'
    }
]

# Create DataFrame
df = pd.DataFrame(switch_data)

# Save to Excel file
excel_filename = 'switchFile.xlsx'
df.to_excel(excel_filename, index=False, engine='openpyxl')

print(f"Created {excel_filename} with {len(switch_data)} sample switches")
print("Please update the file with your actual switch connection details before running the temperature monitoring script.")
print("\nColumns in the Excel file:")
for col in df.columns:
    print(f"  - {col}")