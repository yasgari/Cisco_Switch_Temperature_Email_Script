#!/usr/bin/env python3

import os
import datetime
from checktemp_enhanced import create_pdf_report, analyze_output_for_alerts

def test_normal_temperatures():
    """Test PDF generation with normal temperatures (no critical/catastrophic alerts)"""
    
    # Create sample output with normal temperatures only
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
System Outlet      OK               33
CPU Temperature    OK               39
Power Supply 1     OK               36

 --- Output of show environment temperature on SW-DIST-01 ---
Switch 1 Environment:
Temperature  Status   Reading (Celsius)
-------------+--------+------------------
System Outlet      OK               37
CPU Temperature    OK               44
Power Supply 1     OK               41
Power Supply 2     OK               43

Temperature monitoring completed at: {timestamp}
"""
    
    # Generate timestamp for filenames
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    text_filename = f"device_output_normal_test_{file_timestamp}.txt"
    pdf_filename = f"device_temperature_normal_test_{file_timestamp}.pdf"
    
    # Write text file
    with open(text_filename, 'w') as f:
        f.write(sample_output)
    
    print(f"Testing normal temperature conditions (no critical/catastrophic alerts)")
    print(f"Text file created: {text_filename}")
    
    # Analyze for alerts (should find none)
    warning_hosts, critical_hosts, warning_details, critical_details = analyze_output_for_alerts(sample_output)
    
    if not critical_hosts and not warning_hosts:
        print("✓ No alerts detected - perfect for testing 'NO CRITICAL ALERTS' message")
    else:
        print(f"⚠️ Unexpected alerts found: Critical={critical_hosts}, Warning={warning_hosts}")
    
    # Generate PDF
    success = create_pdf_report(sample_output, pdf_filename, warning_hosts, critical_hosts, warning_details, critical_details)
    
    if success:
        print(f"✓ PDF generated successfully: {pdf_filename}")
        print("✅ The PDF should display 'NO CRITICAL ALERTS AT THIS TIME' in green text at the top")
    else:
        print("❌ Failed to create PDF report")
    
    print(f"\nGenerated files:")
    print(f"  - Text file: {text_filename}")
    print(f"  - PDF file: {pdf_filename}")
    print(f"\nOpen the PDF to verify the 'NO CRITICAL ALERTS AT THIS TIME' message appears in green text!")

if __name__ == "__main__":
    test_normal_temperatures()