#!/usr/bin/env python3

import os
import datetime
from checktemp_enhanced import create_pdf_report, analyze_output_for_alerts

def test_warning_only_temperatures():
    """Test PDF generation with warning temperatures only (no critical/catastrophic alerts)"""
    
    # Create sample output with warning temperatures only
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sample_output = f"""Temperature monitoring started at: {timestamp}

 --- Output of show environment temperature on SW-CORE-01 ---
Switch 1 Environment:
Temperature  Status   Reading (Celsius)
-------------+--------+------------------
System Outlet      OK               35
CPU Temperature    OK               42
Power Supply 1     OK               38
Power Supply 2     OK               40

 --- Output of show environment temperature on SW-ACCESS-01 ---
Switch 1 Environment:
Temperature  Status   Reading (Celsius)
-------------+--------+------------------
System Outlet      WARNING          48
CPU Temperature    OK               39
Power Supply 1     OK               36

 --- Output of show environment temperature on SW-ACCESS-02 ---
Switch 1 Environment:
Temperature  Status   Reading (Celsius)
-------------+--------+------------------
System Outlet      OK               37
CPU Temperature    WARNING          52
Power Supply 1     OK               41
Power Supply 2     OK               43

Temperature monitoring completed at: {timestamp}
"""
    
    # Generate timestamp for filenames
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filename = f"device_output_warning_test_{file_timestamp}.txt"
    pdf_filename = f"device_temperature_warning_test_{file_timestamp}.pdf"
    
    # Write text file
    with open(text_filename, 'w') as f:
        f.write(sample_output)
    
    print(f"Testing warning-only temperature conditions (no critical alerts)")
    print(f"Text file created: {text_filename}")
    
    # Analyze for alerts (should find warnings only)
    warning_hosts, critical_hosts, warning_details, critical_details = analyze_output_for_alerts(sample_output)
    
    if warning_hosts and not critical_hosts:
        print(f"✓ Warning alerts detected on {len(warning_hosts)} switches: {', '.join(warning_hosts)}")
        print("✓ No critical alerts detected - perfect for testing yellow warning status")
    else:
        print(f"⚠️ Unexpected results: Critical={critical_hosts}, Warning={warning_hosts}")
    
    # Generate PDF
    success = create_pdf_report(sample_output, pdf_filename, warning_hosts, critical_hosts, warning_details, critical_details)
    
    if success:
        print(f"✓ PDF generated successfully: {pdf_filename}")
        print("⚠️ The PDF should display 'WARNING CONDITIONS DETECTED' in yellow/orange text at the top")
    else:
        print("❌ Failed to create PDF report")
    
    print(f"\nGenerated files:")
    print(f"  - Text file: {text_filename}")
    print(f"  - PDF file: {pdf_filename}")
    print(f"\nOpen the PDF to verify the yellow 'WARNING CONDITIONS DETECTED' message appears!")

if __name__ == "__main__":
    test_warning_only_temperatures()