#!/usr/bin/env python3
"""
Test version demonstrating alert detection functionality
This creates sample output with warning and critical conditions
"""

import pandas as pd
import datetime
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_output_for_alerts(text_content):
    """
    Analyze switch output for warning/critical conditions
    Returns list of hostnames with alerts and alert summary
    """
    alert_hosts = []
    alert_details = []
    
    sections = text_content.split('\n --- Output of')
    
    for section in sections[1:]:  # Skip first section (timestamp)
        lines = section.split('\n')
        hostname = "Unknown"
        has_alert = False
        
        # Extract hostname from first line
        if lines and 'on ' in lines[0]:
            hostname = lines[0].split(' on ')[-1].strip()
        
        # Check for warning/critical conditions
        for line in lines:
            line_lower = line.lower()
            if 'warning' in line_lower or 'critical' in line_lower:
                has_alert = True
                alert_details.append(f"{hostname}: {line.strip()}")
        
        if has_alert and hostname not in alert_hosts:
            alert_hosts.append(hostname)
    
    return alert_hosts, alert_details

def create_pdf_report(text_content, pdf_filename, alert_hosts=None, alert_details=None):
    """
    Convert text content to PDF format using reportlab
    """
    try:
        logger.info(f"Creating PDF report: {pdf_filename}")
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8,
            spaceAfter=12,
            leftIndent=0,
            rightIndent=0
        )
        
        alert_style = ParagraphStyle(
            'Alert',
            parent=styles['Heading2'],
            textColor='red',
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6
        )
        
        warning_style = ParagraphStyle(
            'Warning',
            parent=styles['Normal'],
            textColor='red',
            fontSize=10,
            leftIndent=20,
            spaceAfter=3
        )
        
        # Build story for PDF
        story = []
        
        # Add title
        title_style = styles['Title']
        title = Paragraph("Cisco Switch Temperature Monitoring Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add alert summary if there are any alerts
        if alert_hosts and len(alert_hosts) > 0:
            story.append(Paragraph("⚠️ TEMPERATURE ALERTS DETECTED", alert_style))
            story.append(Paragraph(f"Affected Switches: {', '.join(alert_hosts)}", warning_style))
            story.append(Spacer(1, 6))
            
            if alert_details:
                story.append(Paragraph("Alert Details:", styles['Heading3']))
                for detail in alert_details:
                    story.append(Paragraph(f"• {detail}", warning_style))
            
            story.append(Spacer(1, 20))
            story.append(Paragraph("Detailed Report:", styles['Heading2']))
            story.append(Spacer(1, 12))
        
        # Split content into sections and add to PDF
        sections = text_content.split('\n --- Output of')
        
        for i, section in enumerate(sections):
            if i == 0:
                # First section contains the start time
                story.append(Paragraph(section.strip(), styles['Normal']))
                story.append(Spacer(1, 12))
            else:
                # Restore the split delimiter and format as code
                section_content = " --- Output of" + section
                # Split into lines and create preformatted text
                lines = section_content.split('\n')
                for line in lines:
                    if line.strip():
                        # Highlight lines with warnings/critical in red
                        line_lower = line.lower()
                        if 'warning' in line_lower or 'critical' in line_lower:
                            story.append(Paragraph(f"<font color='red'>{line}</font>", styles['Normal']))
                        else:
                            story.append(Preformatted(line, code_style))
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF report created successfully: {pdf_filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating PDF report: {str(e)}")
        return False

def main():
    """
    Test version demonstrating alert detection
    """
    ts = time.time()
    
    logger.info("Testing alert detection with sample data containing warnings and critical conditions")
    
    time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    timestamp_safe = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    
    # Create sample output with alerts to test detection
    outputsVar = f'Start Script at Time: {time_str}\n'
    
    # Normal switch
    normal_output = """Temperature Status: Ok
Sensor                 Status          Reading
System Inlet           OK              23 Celsius
System Outlet          OK              28 Celsius
CPU Temperature        OK              42 Celsius
Power Supply 1         OK              35 Celsius
Power Supply 2         OK              33 Celsius"""
    
    # Switch with warning
    warning_output = """Temperature Status: Warning
Sensor                 Status          Reading
System Inlet           OK              23 Celsius
System Outlet          WARNING         45 Celsius
CPU Temperature        OK              42 Celsius
Power Supply 1         OK              35 Celsius
Power Supply 2         OK              33 Celsius"""
    
    # Switch with critical condition
    critical_output = """Temperature Status: Critical
Sensor                 Status          Reading
System Inlet           OK              23 Celsius
System Outlet          CRITICAL        65 Celsius
CPU Temperature        WARNING         58 Celsius
Power Supply 1         OK              35 Celsius
Power Supply 2         CRITICAL        72 Celsius"""
    
    # Add outputs for different switches
    outputsVar += f'\n --- Output of show env temp on SW-CORE-01 \n{normal_output}\n\n'
    outputsVar += f'\n --- Output of show env temp on SW-ACCESS-02 \n{warning_output}\n\n'
    outputsVar += f'\n --- Output of show env temp on SW-DIST-03 \n{critical_output}\n\n'
    
    # Test alert detection
    alert_hosts, alert_details = analyze_output_for_alerts(outputsVar)
    
    # Generate output files
    text_filename = f'device_output_alert_test_{timestamp_safe}.txt'
    pdf_filename = f'device_temperature_alert_test_{timestamp_safe}.pdf'
    
    # Write text output
    logger.info(f"Writing text output to: {text_filename}")
    with open(text_filename, 'w') as f:
        f.write(outputsVar)
    
    # Display alert detection results
    if alert_hosts:
        logger.warning(f"Alert detection test: Found alerts on {len(alert_hosts)} switches: {', '.join(alert_hosts)}")
        logger.info("Alert details:")
        for detail in alert_details:
            logger.info(f"  - {detail}")
    else:
        logger.info("Alert detection test: No alerts found")
    
    # Create PDF report with alert highlighting
    pdf_success = create_pdf_report(outputsVar, pdf_filename, alert_hosts, alert_details)
    
    if pdf_success:
        logger.info("Alert detection test completed successfully!")
        logger.info(f"Generated files:")
        logger.info(f"  - Text file: {text_filename}")
        logger.info(f"  - PDF file: {pdf_filename}")
        
        print(f"\nAlert Detection Test Results:")
        print(f"✓ Text file created: {text_filename}")
        print(f"✓ PDF file created: {pdf_filename}")
        if alert_hosts:
            print(f"🚨 ALERTS DETECTED on switches: {', '.join(alert_hosts)}")
            print(f"📧 Email would have alert subject: '🚨 ALERT: Cisco switch device temperature update {time_str} - Issues on {', '.join(alert_hosts)}'")
        else:
            print(f"✓ No alerts detected - normal email would be sent")
    else:
        logger.error("PDF generation failed")
        print("✗ PDF generation failed")

if __name__ == "__main__":
    main()